#!/usr/bin/env python
import json

from lxml import etree


class Response(object):
    """
    Return a friendly response
    """

    def __init__(self, url: str, *,
                 meta: dict,
                 content: bytes = b'',
                 cookies,
                 history,
                 headers: dict = None,
                 status: int):
        self._callback_result = None
        self.__url = url
        self.__content = content
        self.__meta = meta
        self.__cookies = cookies
        self.__history = history
        self.__headers = headers
        self.__status = status
        self.__text = None
        self.__json = None

    @property
    def callback_result(self):
        return self._callback_result

    @callback_result.setter
    def callback_result(self, value):
        self._callback_result = value

    @property
    def url(self):
        return self.__url

    @property
    def meta(self):
        return self.__meta

    @property
    def cookies(self):
        return self.__cookies

    @property
    def history(self):
        return self.__history

    @property
    def headers(self):
        return self.__headers

    @property
    def status(self):
        return self.__status

    @property
    def text(self):
        if self.__text is None:
            self.__text = self.__content.decode()
        return self.__text

    @property
    def json(self):
        if self.__json is None:
            try:
                self.__json = json.loads(self.__content)
            except json.decoder.JSONDecodeError:
                return None
        return self.__json

    @property
    def html_etree(self):
        html_etree = etree.HTML(self.text)
        return html_etree

    def __str__(self):
        return f'<Response url: {self.__url} status:{self.__status} meta:{self.__meta}>'
