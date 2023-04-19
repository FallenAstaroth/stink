from io import BytesIO
from uuid import uuid4
from sys import hexversion
from codecs import getencoder
from mimetypes import guess_type
from typing import Union, List, Tuple, BinaryIO


class MultipartFormDataEncoder(object):
    """
    Creates a multipart/form-data content type.
    """

    def __init__(self, errors: bool):
        self.__errors = errors
        self.__boundary = uuid4().hex

    @classmethod
    def u(cls, string: Union[str, bytes]) -> str:
        """
        Decodes the string.
        :param string: str|bytes
        :return: str
        """
        if hexversion < 0x03000000 and isinstance(string, str):
            string = string.decode("utf-8")

        if hexversion >= 0x03000000 and isinstance(string, bytes):
            string = string.decode("utf-8")

        return string

    def iter(self, fields: List[Tuple[str, Union[str, int]]], files: List[Tuple[str, str, BinaryIO]]) -> str:
        """
        Writes fields and files to the body.
        :param fields: [(str, str|int)]
        :param files: [(str, str, BinaryIO)]
        :return: str
        """
        encoder = getencoder("utf-8")

        for (key, value) in fields:

            key = self.u(key)

            yield encoder(f"--{self.__boundary}\r\n")
            yield encoder(self.u(f'Content-Disposition: form-data; name="{key}"\r\n\r\n'))

            if isinstance(value, int) or isinstance(value, float):
                value = str(value)

            yield encoder(self.u(f"{value}\r\n"))

        for (key, filename, filedata) in files:

            key = self.u(key)
            filename = self.u(filename)

            yield encoder(f"--{self.__boundary}\r\n")
            yield encoder(self.u(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'))
            yield encoder(f"Content-Type: {guess_type(filename)[0] or 'application/octet-stream'}\r\n\r\n")

            buffer = filedata.read()

            yield buffer, len(buffer)
            yield encoder("\r\n")

        yield encoder(f"--{self.__boundary}--\r\n")

    def encode(self, fields: List[Tuple[str, Union[str, int]]], files: List[Tuple[str, str, BinaryIO]]) -> Tuple[str, bytes]:
        """
        Converts specified files and fields to multipart/form-data format.
        :param fields: [(str, str|int)]
        :param files: [(str, str, BinaryIO)]
        :return: (str, bytes)
        """
        try:

            body = BytesIO()

            for chunk, chunk_len in self.iter(fields, files):
                body.write(chunk)

            return f"multipart/form-data; boundary={self.__boundary}", body.getvalue()

        except Exception as e:
            if self.__errors is True: print(f"[Form]: {repr(e)}")
