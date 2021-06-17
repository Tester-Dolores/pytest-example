import wave
import base64
import json
from locust import  User, task,HttpUser,between
from utils.help import api_data
from utils.ws_request import WSRequest
from utils.http_request import MySession, MyFastSession
from locust.contrib.fasthttp import FastHttpUser

"""
class WebSocketLocust1(User):
    wait_time = between(5, 9)

    def __init__(self, *args, **kwargs):
        super(WebSocketLocust1, self).__init__(*args, **kwargs)
        params = api_data()["params"]
        self.client = WSRequest(api_data()["wsurl"],params)

    def on_start(self):
        print('--------- task start ------------')

    def on_stop(self):
        print('---------- task stop ------------')

    @task
    def test_ws(self):
        wav ="./wav/A11_0.wav"
        self.client.start(wav)


class WebSocketLocust2(HttpUser):
    wait_time = between(5, 9)

    def __init__(self, *args, **kwargs):
        super(WebSocketLocust2, self).__init__(*args, **kwargs)
        self.client = MySession()
        self.client.headers = {"Accept": "application/json"}


    def on_start(self):
        print('--------- task start ------------')

    def on_stop(self):
        print('---------- task stop ------------')

    @task
    def test_geocode(self):
        url = api_data()["geocode_geo"]["api"]+"address="+api_data()["geocode_geo"]["address"]+"&key="+api_data()['key']

        self.client.get(url)

"""

class HttpLocust(FastHttpUser):
    wait_time = between(0, 1)

    def __init__(self, environment, *args, **kwargs):
        super(HttpLocust, self).__init__(environment, *args, **kwargs)
        self.client = MyFastSession(environment, self)
        self.client.headers = {"Accept": "application/json"}

    def on_start(self):
        print("--------- task start ------------")

    def on_stop(self):
        print("---------- task stop ------------")

    @task
    def test_geocode(self):
        url = api_data()["geocode_geo"]["api"]+"address="+api_data()["geocode_geo"]["address"]+"&key="+api_data()['key']

        self.client.get(url)

