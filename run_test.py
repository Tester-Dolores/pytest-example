import pytest
import time
import os

debug = False
CASE_DIR = "./testcase"
REPORT_DIR = "./report"

if __name__ == "__main__":
    html_report = os.path.join(
        REPORT_DIR, time.strftime("%Y%m%d%H%M%S") + "report.html"
    )
    if debug:
        pytest.main(["-s", "-v", "--pdb", CASE_DIR, "-m", marked])
    else:
        pytest.main(
            [
                "-s",
                "-vv",
                CASE_DIR,
                "--reruns",
                "0",
                "--html=" + html_report,
                "--self-contained-html",
            ]
        )
