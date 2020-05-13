import os
import time
from core.HTMLTestRunner_cn import HTMLTestRunner
from unittest import defaultTestLoader


def run(case_path):
    path = os.getcwd()
    report_path = path + "/report"
    if not os.path.exists(report_path):
        os.mkdir(report_path)
    cases = defaultTestLoader.discover(case_path, pattern="test_*.py")
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())  # 生成一个年月日时分秒的时间戳
    report_path = path + "/report/自动化测试报告" + time_str + ".html"
    print(report_path)
    with open(report_path, "wb") as f:
        h = HTMLTestRunner(f, verbosity=2, title="接口自动化")
        h.run(cases)
