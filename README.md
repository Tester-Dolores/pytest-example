ubuntu 18.04 LTS
安装依赖
```
pipenv shell
pipenv sync
```
# 执行接口测试

`python run_test.py`

http执行结果
```
(pytest-example) test@LAPTOP-3NQL6G6U /mnt/d/pytest-example (main) $ python run_test.py
================================================= test session starts ==================================================
platform linux -- Python 3.7.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1 -- /home/hxe/.local/share/virtualenvs/pytest-example-vuC_Kfz-/bin/python
cachedir: .pytest_cache
metadata: {'Python': '3.7.5', 'Platform': 'Linux-4.4.0-19041-Microsoft-x86_64-with-Ubuntu-18.04-bionic', 'Packages': {'pytest': '6.2.4', 'py': '1.10.0', 'pluggy': '0.13.1'}, 'Plugins': {'html': '3.1.1', 'metadata': '1.11.0', 'rerunfailures': '10.0'}, '项目名称': '高德地图API测试'}
rootdir: /mnt/d/pytest-example
plugins: html-3.1.1, metadata-1.11.0, rerunfailures-10.0
collected 4 items

testcase/test_direction.py::TestDirection::test_direction_walking PASSED
testcase/test_direction.py::TestDirection::test_direction_transit PASSED
testcase/test_geocode.py::TestGeocode::test_geo PASSED
testcase/test_geocode.py::TestGeocode::test_regeo PASSED

=================================================== warnings summary ===================================================
testcase/test_direction.py::TestDirection::test_direction_walking
testcase/test_direction.py::TestDirection::test_direction_transit
testcase/test_geocode.py::TestGeocode::test_geo
testcase/test_geocode.py::TestGeocode::test_regeo
  /home/hxe/.local/share/virtualenvs/pytest-example-vuC_Kfz-/lib/python3.7/site-packages/urllib3/connectionpool.py:1020: InsecureRequestWarning: Unverified HTTPS request is being made to host 'localhost'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    InsecureRequestWarning,

-- Docs: https://docs.pytest.org/en/stable/warnings.html
------------------ generated html file: file:///mnt/d/pytest-example/report/20210604001857report.html ------------------
============================================ 4 passed, 4 warnings in 0.56s =============================================
```


# 执行性能测试

[websocket接口 前置步骤]
**目前已经改为 讯飞语音识别接口,但是locust对应的配置还未调整,因此不确定是否能够执行**
1. 更改配置文件 api_data.yaml ws data 相关配置
2. 调试 ws_request.py on_open()方法的run()方法,直到可以正确发送data
3. 调试 ws_request.py on_message()方法,直到可以正确打印数据

* 已经有在本地跑过确认可以正确连接websocket服务器和启动locust执行性能测试

[执行]

`locust`

如果`./report/locustlog.txt`打印如下,即说明已启动服务. 此时请使用浏览器打开'http://127.0.0.1:8089'

```
[2021-06-16 20:45:19,378] LAPTOP-3NQL6G6U/WARNING/locust.main: System open file limit '1024' is below minimum setting '10000'. It's not high enough for load testing, and the OS didn't allow locust to increase it by itself. See https://github.com/locustio/locust/wiki/Installation#increasing-maximum-number-of-open-files-limit for more info.
[2021-06-16 20:45:19,379] LAPTOP-3NQL6G6U/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2021-06-16 20:45:19,390] LAPTOP-3NQL6G6U/INFO/locust.main: Starting Locust 1.5.3

```

**如果您有任何问题...请先google...**

**If you have any questions... Please Google first...**
