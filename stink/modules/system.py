from wmi import WMI
from mss import mss
from os import mkdir
from getpass import getuser
from psutil import process_iter
from datetime import datetime
from socket import gethostbyname, gethostname


class System:

    def __init__(self, *args):

        for index, variable in enumerate(["storage_path", "storage_folder", "folder", "statuses", "errors"]):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        if any(self.statuses):
            mkdir(f"{self.storage_path}{self.storage_folder}{self.folder}")

    def __create_screen(self):

        if self.statuses[0] is True:

            with mss() as screen:
                screen.shot(mon=-1, output=f"{self.storage_path}{self.storage_folder}{self.folder}/Screenshot.png")

    def __get_system_info(self):

        if self.statuses[1] is True:

            computer = WMI()

            os_info = computer.Win32_OperatingSystem()[0]
            cpu_info = computer.Win32_Processor()[0]
            gpu_info = computer.Win32_VideoController()[0]

            info = (
                f"User: {getuser()}\n",
                f"IP: {gethostbyname(gethostname())}\n",
                f"OS Name: {os_info.Name.split('|')[0]}\n",
                f"OS Version: {' '.join([os_info.Version, os_info.BuildNumber])}\n",
                f"CPU: {cpu_info.Name}\n",
                f"GPU: {gpu_info.Name}\n",
                f"RAM: {round(float(os_info.TotalVisibleMemorySize) / 1048576)} GB\n"
            )

            with open(f"{self.storage_path}{self.storage_folder}{self.folder}/Configuration.txt", "a", encoding="utf-8") as system:

                for item in info:
                    system.write(item)

            system.close()

    def __get_system_processes(self):

        if self.statuses[2] is True:

            with open(f"{self.storage_path}{self.storage_folder}{self.folder}/Processes.txt", "a", encoding="utf-8") as processes:

                processes.write(f"[Startup time] [Status] [CPU %] [RAM %] [Name]\n")

                for process in process_iter():
                    processes.write(f"\n[{datetime.fromtimestamp(process.create_time())}] [{process.status()}] [{process.cpu_percent()}] [{process.memory_percent():.4f}] {process.name()}")

            processes.close()

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()
            self.__get_system_info()
            self.__get_system_processes()

        except Exception as e:

            if self.errors is True:
                print(f"[SYSTEM]: {repr(e)}")
