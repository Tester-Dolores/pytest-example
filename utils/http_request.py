from locust.clients import HttpSession
from locust.contrib.fasthttp import FastHttpSession
from utils.help import api_data
from locust import events


class MySession(HttpSession):
    proxies = None
    if api_data()["is_use_fiddler"]:
        proxies = {"http": "localhost:8888", "https": "localhost:8888"}

    def __init__(self, request_event=events.request, user="", *args, **kwargs):
        super().__init__(
            base_url="", request_event=request_event, user=user, *args, **kwargs
        )

    def request(self, method, url, proxies=proxies, verify=False, *args, **kwargs):
        global resp
        if url.startswith("/"):
            url = api_data()["api_data"]["url"] + url

        resp = super(MySession, self).request(
            method,
            url,
            proxies=proxies,
            verify=verify,
            timeout=(3, 180),
            *args,
            **kwargs
        )
        return resp


class MyFastSession(FastHttpSession):
    proxies = None
    if api_data()["is_use_fiddler"]:
        proxies = {"http": "localhost:8888", "https": "localhost:8888"}

    def __init__(self, environment, user, *args, **kwargs):
        super().__init__(
            base_url="", environment=environment, user=user, *args, **kwargs
        )

    def request(self, method, url, proxies=proxies, verify=False, *args, **kwargs):
        global resp
        if url.startswith("/"):
            url = api_data()["api_data"]["url"] + url

        resp = super(MyFastSession, self).request(
            method,
            url,
            proxies=proxies,
            verify=verify,
            timeout=(3, 180),
            *args,
            **kwargs
        )
        return resp
