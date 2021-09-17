from mss import mss


class Screen_Grabber:

    def __init__(self, storage_path: str, storage_folder: str, errors_print: bool):

        self.storage_path = storage_path
        self.storage_folder = storage_folder
        self.errors_print = errors_print

    def __create_screen(self):

        with mss() as screen:
            screen.shot(mon=-1, output=f"{self.storage_path}{self.storage_folder}screenshot.png")

    def run(self):

        try:

            self.__create_screen()

        except Exception as e:

            if self.errors_print is True:

                print(f"[SCREEN_GRABBER]: {repr(e)}")

            else:

                pass
