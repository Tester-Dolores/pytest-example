import time
from requests import Session
from utils.help import events_request



class MySession(Session):
    
    proxies = None
    verify = None
    """
    proxies={"http":"localhost:8888","https":"localhost:8888"}
    verify = False
    """
    def request(self, method, url, proxies=proxies, verify=verify, *args, **kwargs):
        global resp
        start_time = time.time()

        resp = super(MySession, self).request(
            method,
            url,
            proxies=proxies,
            verify=verify,
            timeout=(3, 180),
            *args,
            **kwargs
        )

        total_time = int((time.time() - start_time) * 1000)
        events_request("success",method, url.split("/")[-1],resp.text, total_time)

        return resp