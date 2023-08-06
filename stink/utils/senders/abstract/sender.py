from abc import abstractmethod
from typing import Tuple, Union

from stink.helpers.config import SenderConfig


class AbstractSender:
    """
    Template for the sender.
    """
    def __init__(self):

        self.__zip_name = None
        self.__storage_path = None

        self._config = SenderConfig()

    @abstractmethod
    def __get_sender_data(self) -> Tuple[Union[str, bytes], ...]:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of data.
        """
        ...

    @abstractmethod
    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        ...

    @abstractmethod
    def run(self, zip_name: str, storage_path: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - storage_path [str]: Path to storage.

        Returns:
        - None.
        """
        ...
