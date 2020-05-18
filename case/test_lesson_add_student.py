from core import *


class AddStudentTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.student = Student.of("yjq").default()
        cls.jigou = Jigou.of("yjq").default()

    def test_del_student(self):
        """删除学生"""
        data = {
            "orgId": self.jigou.userId,
            "teacherId": self.student.userId,
            "deleteType": "1",
            "token": self.jigou.token
        }
        res = Mizhu.web_usr_orgDelTeacher().post(data)
        assert res.json()["code"] == "200"

    def test_add_student(self):
        """添加学生"""
        data = {
            "account": self.student.account,
            "orgId": self.jigou.orgId,
            "token": self.jigou.token
        }
        res = Mizhu.web_orgInfo_addStudentToOrg().post(data)
        json = res.json()
        assert json["code"] == "200"
        assert json["data"]["userList"][0]["account"] == self.student.account
        assert json["data"]["userList"][0]["userId"] == str(self.student.userId)

    def test_search(self):
        """搜索学生功能"""
        data = {
            "currentPage": 1,
            "phone": "",
            "name": self.student.nickname,
            "pageSize": "10",
            "token": self.jigou.token
        }

        res = Mizhu.web_orgInfo_orgStudentList().post(data)
        json = res.json()
        assert json["code"] == "200"
        assert json["data"]["list"][0]["account"] == self.student.account
        assert json["data"]["list"][0]["userId"] == str(self.student.userId)
        assert json["data"]["list"][0]["nickname"] == self.student.nickname
