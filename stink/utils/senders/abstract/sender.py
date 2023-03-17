from abc import abstractmethod

from stink.helpers.config import SenderConfig


class AbstractSender:

    def __init__(self):
        self._config = SenderConfig()

    @abstractmethod
    def __get_sender_data(self):
        ...

    @abstractmethod
    def __send_archive(self):
        ...

    @abstractmethod
    def run(self, zip_name: str, storage_path: str, errors: bool):
        ...
