from core import *
# from unittest import TestCase
import ddt


class SampleExample(TestCase):
    """简单测试"""

    def test_login(self):
        """登录测试"""

        data = {
            "userName": "robot0001",
            "password": "111111"
        }
        res = Mizhu.web_usr_login().post(data=data)
        assert res.json()["code"] == "200"

    def test_login_f(self):
        """登录测试 密码错误"""

        data = {
            "userName": "robot0001",
            "password": "aa"
        }
        res = Mizhu.web_usr_login().post(data=data)
        assert res.json()["code"] == "200"


@ddt.ddt
class DttExample(TestCase):
    """数据驱动例子"""

    @ddt.data("robot0001", "asdasdasd")
    def test_login_for_account(self, account):
        """登录测试"""

        data = {
            "userName": account,
            "password": "111111"
        }
        res = Mizhu.web_usr_login().post(data=data)
        token = res.json()["token"]
        assert token, "token有误"

    @ddt.unpack
    @ddt.data(["robot0001", "111111"], ["robot0002", "asdasdasd"])
    def test_login_for_account_password(self, account, password):
        """登录测试"""

        data = {
            "userName": account,
            "password": password
        }
        res = Mizhu.web_usr_login().post(data=data)
        token = res.json()["token"]
        assert token, "token有误"
