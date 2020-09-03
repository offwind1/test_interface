from core import *
from core.util.userUtil import UserUtil
from core.util.phoneCodeUtil import PhoneCodeUtil


class Org:
    pass


close_org = Org()
close_org.orgId = "8628"

open_org = Org()
open_org.orgId = "8445"


class TestUserLogin(TestCase):

    def test_001(self):
        student = Student.of("yjq").default()
        AuthFlow(student, open_org, close_org).run()

    def test_002(self):
        jigou = Jigou.of("yjq").default()
        clazz = Clazz.findClass(jigou, "新建班级")

        se = StudentExecl()
        account = random_str(6)
        password = "111111"
        se.add(account, account, password)
        clazz.add_student_by_execl(se)

        student = Student.of("yjq").login(account, password)
        AuthFlow(student, open_org, close_org).run()

    def test_003(self):
        jigou = Jigou.of("yjq").login("tester002", "111111")
        clazz = Clazz.findClass(jigou, "新建班级")

        se = StudentExecl()
        account = random_str(6)
        password = "111111"
        se.add(account, account, password)
        clazz.add_student_by_execl(se)

        student = Student.of("yjq").login(account, password)
        AuthFlow(student, open_org, close_org).run()

    def test_004(self):
        admin = Admin.of("yjq").default()
        account = random_str(6)
        password = "111111"
        json = Manage.web_usr_addNewUser().post({
            "account": account,
            "password": password,
            "nickname": account,
            "sex": "M",
            "identity": "0",
            "safeQuestionId": "1",
            "safeAnswer": "大BOSS",
            "tag": "",
            "token": admin.token
        }).json()

        assertPass(json)
        student = Student.of("yjq").login(account, password)
        AuthFlow(student, open_org, close_org).run()


class AuthFlow():

    def __init__(self, usr: Student, open_org, close_org):
        self.usr = usr
        self.open_org = open_org
        self.close_org = close_org

    def run(self):
        self.login_8orange()
        self.login_open_org()
        self.login_close_org()

    def login(self, org):
        return Mizhu.api_mobile_login().post({
            "account": self.usr.account,
            "password": self.usr.password,
            "phone": "",
            "verifycode": "",
            "loginMode": "3",
            "proType": "yk",
            "orgId": org,
            "machine": "web",
        }).json()

    def login_8orange(self):
        json = self.login("0")
        assertPass(json)

    def login_open_org(self):
        json = self.login(self.open_org.orgId)
        assertPass(json)

    def login_close_org(self):
        json = self.login(self.close_org.orgId)
        list = [str(x["schoolId"]) for x in self.usr.data["data"]["orgRelList"]]
        if close_org.orgId in list:
            assertPass(json)
        else:
            assertValueEqule(json["msg"], "您的账号不在授权范围内，请联系学校教务处!")
