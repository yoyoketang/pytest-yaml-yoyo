import requests
import re
from requests import Response
from . import exceptions


class HttpSession(requests.Session):

    def __init__(self, base_url: str = None, timeout=10):
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout

    @staticmethod
    def check_url(base_url: str, url: str) -> str:
        """ 拼接base_url 和 url 地址"""
        if re.compile(r"(http)(s?)(://)").match(url):
            return url
        elif base_url:
            if re.compile(r"(http)(s?)(://)").match(base_url):
                return f"{base_url.rstrip('/')}/{url.lstrip('/')}"
            else:
                raise exceptions.ParserError("base url do yo mean http:// or https://!")
        else:
            raise exceptions.ParserError("url invalid or base url missed!")

    def send_request(self, method, url, base_url=None, **kwargs) -> Response:
        """
            发送 request 请求
        :param method: 请求方式
        :param url: url 地址
        :param base_url: 环境地址
        :param kwargs: 其它参数
        :return: Response
        """
        if base_url:
            url = self.check_url(base_url, url)
            return self.request(method, url, timeout=self.timeout, **kwargs)
        else:
            url = self.check_url(self.base_url, url)
            return self.request(method, url, timeout=self.timeout, **kwargs)
