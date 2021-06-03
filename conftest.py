from requests import Session
import yaml
import pytest

with open("./data/apidata.yaml", encoding="UTF-8", errors="ignore") as f:
    api_data = yaml.load(f, Loader=yaml.SafeLoader)
key = api_data['key']

class MySession(Session):
    """
    proxies = None
    verify = None
    """
    proxies={"http":"localhost:8888","https":"localhost:8888"}
    verify = False
    
    def request(self, method, url, proxies=proxies, verify=verify, *args, **kwargs):
        global resp
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

@pytest.fixture(scope="session")
def req():
    request = MySession()
    request.headers = {"Accept": "application/json"}

    return request


@pytest.mark.hookwrapper(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    description = description_html(item.function.__doc__)
    extra = getattr(report, "extra", [])
    desc_html = "<p>Description:%s;</p>" % (description)
    extra.append(pytest_html.extras.html(desc_html))
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            html = "<p>123</p>"
            """
            html = (
                "<div><p>Request URL:%s;</p>"
                "<p>Response:%s</p>"
                "<p>Request body:%s</p>"
                "<p>Request header:%s</p></div>"
                % (
                    resp.request.url,
                    resp.json(),
                    resp.request.body,
                    resp.request.headers,
                )
            )
            """
            extra.append(pytest_html.extras.html(html))
        report.extra = extra


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == "\n":
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(html.meta(name="Content-Type", value="text/html; charset=utf-8")),
        html.body([html.p(line) for line in desc_lines]),
    )
    return desc_html

def pytest_configure(config):
    config._metadata["项目名称"] = "高德地图API测试"