from core import *
from core.util.phoneCodeUtil import PhoneCodeUtil
from core.util.userUtil import UserUtil


class TestUserInfo(TestCase):
    phone_poll = ["17043763124",
                  "17043763122",
                  "17043763121",
                  "17043763120",
                  "17043763119",
                  "17043763118",
                  "17043763117",
                  "15263819409",
                  "17043763116",
                  "17043763115",
                  "17043763145",
                  "17043763144",
                  "17043763143",
                  "17043763142",
                  "17043763141",
                  "17043763140",
                  "17043763139",
                  "17043763138",
                  "17043763137",
                  "17043763136",
                  ]

    # @classmethod
    # def setUpClass(cls) -> None:
    #     for phone in cls.phone_poll:
    #         data = PhoneCodeUtil.get_code(phone, PhoneCodeUtil.LOGIN)
    #         if data is not None and data != "null":
    #             cls.phone = phone
    #             cls.verifycode = data
    #             break

    def find_phone(self):
        for phone in self.phone_poll:
            data = PhoneCodeUtil.get_code(phone, PhoneCodeUtil.LOGIN)
            if data is not None and data != "null":
                self.phone = phone
                self.verifycode = data
                break


    def test_002(self):
        # UserUtil.delete_user_by_search(phone=self.phone)
        self.find_phone()
        UserUtil.delete_user_phone(self.phone)

        # 带昵称信息，班级和年级信息注册
        json = Mizhu.api_mobile_login().post({
            "account": "",
            "password": "",
            "longitude": "",
            "latitude": "",
            "phone": self.phone,
            "verifycode": self.verifycode,
            "gradeId": "9",
            "userName": "王小发",
            "stuName": "四班",

        }).json()
        assertPass(json)
        data = json["data"]

        assertValueEqule(data["name"], "王小发")
        assertValueEqule(data["nickname"], "王小发")

    def test_1(self):
        # UserUtil.delete_user_by_search(phone=self.phone)
        self.find_phone()
        UserUtil.delete_user_phone(self.phone)

        # 手机号新注册账号
        json = Mizhu.api_mobile_login().post({
            "account": "",
            "password": "",
            "longitude": "",
            "latitude": "",
            "phone": self.phone,
            "verifycode": self.verifycode,
            "machine": "python test",
            "proType": "ykdebug"
        }).json()
        assertPass(json)
        data = json["data"]
        # 新注册账号验证
        self.assert_new_req(data)
        account = data["account"]
        token = data["token"]
        userId = data["userId"]
        password = "111111"

        # 修改密码
        json = Mizhu.api_mobile_updatePassword().post({
            "oldPassword": password,
            "newPassword": password,
            "token": token
        }).json()
        assertPass(json)
        assertValueEqule(json['msg'], "更新密码成功！")

        # 账号认证
        UserUtil.reply_user(userId)

        # 账号密码登录
        student = Student.of("yjq").login(account, password)
        self.assert_teacher(student.data["data"])

    def assert_teacher(self, data):
        # 新注册账号，需要有账号
        assertValueIsNotNull(data["account"])

        # 新注册账号未认证
        assertValueEqule(data["authen"], "2")
        assertValueEqule(data["authenResult"], "0")
        assertValueEqule(data["authenStatus"], "已认证")

        # 新注册账号，分配了云信账号
        assertValueIsNotNull(data["cloudUsrAccount"])
        assertValueIsNotNull(data["cloudUsrId"])

        # 新注册账号，默认有30米猪时光
        assertValueEqule(data["mizhuTime"], "30.0")

        # 新注册账号,昵称不为空
        assertValueIsNotNull(data["nickname"])

        # orgId 为 0
        assertValueEqule(data['orgId'], "0")
        assertValueIsNull(data["orgMsgList"])

        # status is 1
        assertValueEqule(data["status"], "1")

        # userIdentity is 0
        assertValueEqule(data["userIdentity"], "0")
        assertValueEqule(data["userIdentityValue"], "个人")

        # phone check
        assertValueEqule(data['userPhone'], self.phone)

        # 用户类型
        assertValueEqule(data['userType'], "3")
        assertValueEqule(data['userTypeValue'], "学生")

    def assert_new_req(self, data):
        # 新注册账号，需要有账号
        assertValueIsNotNull(data["account"])

        # 新注册账号未认证
        assertValueEqule(data["authen"], "0")
        assertValueEqule(data["authenResult"], "0")
        assertValueEqule(data["authenStatus"], "未认证")

        # 新注册账号，分配了云信账号
        assertValueIsNotNull(data["cloudUsrAccount"])
        assertValueIsNotNull(data["cloudUsrId"])

        # 新注册账号，默认有30米猪时光
        assertValueEqule(data["mizhuTime"], "30.0")

        # 新注册账号,昵称不为空
        assertValueIsNotNull(data["nickname"])

        # orgId 为 0
        assertValueEqule(data['orgId'], "0")
        assertValueIsNull(data["orgMsgList"])

        # status is 1
        assertValueEqule(data["status"], "1")

        # userIdentity is 0
        assertValueEqule(data["userIdentity"], "0")
        assertValueEqule(data["userIdentityValue"], "个人")

        # phone check
        assertValueEqule(data['userPhone'], self.phone)

        # 用户类型
        assertValueEqule(data['userType'], "3")
        assertValueEqule(data['userTypeValue'], "学生")
