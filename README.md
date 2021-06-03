ubuntu 18.04 LTS
1. 安装依赖
```
pipenv shell
pipenv sync
```
2. python run_test.py
执行结果
```
(pytest-example) hxe@LAPTOP-3NQL6G6U /mnt/d/pytest-example (main) $ python run_test.py
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
