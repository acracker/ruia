#!/usr/bin/env python
import json

from lxml import etree


class Response(object):
    """
    Return a friendly response
    """

    def __init__(self, url: str, *,
                 metadata: dict,
                 content: bytes = b'',
                 cookies,
                 history,
                 headers: dict = None,
                 status: int):
        self._callback_result = None
        self._url = url
        self._content = content
        self._metadata = metadata
        self._cookies = cookies
        self._history = history
        self._headers = headers
        self._status = status
        self._text = None
        self._json = None

    @property
    def callback_result(self):
        return self._callback_result

    @callback_result.setter
    def callback_result(self, value):
        self._callback_result = value

    @property
    def url(self):
        return self._url

    @property
    def metadata(self):
        return self._metadata

    @property
    def cookies(self):
        return self._cookies

    @property
    def history(self):
        return self._history

    @property
    def headers(self):
        return self._headers

    @property
    def status(self):
        return self._status

    @property
    def text(self):
        if self._text is None:
            self._text = self._content.decode()
        return self._text

    @property
    def json(self):
        if self._json is None:
            try:
                self._json = json.loads(self._content)
            except json.decoder.JSONDecodeError:
                return None
        return self._json

    @property
    def html_etree(self):
        html_etree = etree.HTML(self.text)
        return html_etree

    def __str__(self):
        return f'<Response url: {self._url} status:{self._status} metadata:{self._metadata}>'
