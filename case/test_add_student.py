from core import *


class AddStudentTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.student = Student.of("yjq").default()
        cls.jigou = Jigou.of("yjq").default()


    def test_1(self):
        """测试"""
        print("测试输出")



    def test_del_student(self):
        """删除学生"""
        data = {
            "orgId": self.jigou.userId,
            "teacherId": self.student.userId,
            "deleteType": "1",
            "token": self.jigou.token
        }
        res = Mizhu.web_usr_orgDelTeacher().post(data)
        assertPass(res)
        # assert res.json()["code"] == "200"

    def test_add_student(self):
        """添加学生"""
        data = {
            "account": self.student.account,
            "orgId": self.jigou.orgId,
            "token": self.jigou.token
        }
        res = Mizhu.web_orgInfo_addStudentToOrg().post(data)
        json = res.json()
        assertPass(json)
        assert json["data"]["userList"][0]["account"] == self.student.account
        assert json["data"]["userList"][0]["userId"] == str(self.student.userId)

    def test_search(self):
        """搜索学生功能"""
        """未加入班级的学生，是否显示"""
        data = {
            "currentPage": 1,
            "phone": "",
            "name": self.student.nickname,
            "pageSize": "10",
            "token": self.jigou.token
        }

        res = Mizhu.web_orgInfo_orgStudentList().post(data)
        json = res.json()
        assertPass(json)
        assert json["data"]["list"][0]["account"] == self.student.account
        assert json["data"]["list"][0]["userId"] == str(self.student.userId)
        assert json["data"]["list"][0]["nickname"] == self.student.nickname

    def test_student_orgId(self):
        """学生加入机构后，个人信息中有机构id"""
        self.student = Student.of("yjq").default(refresh=True)
        assert self.jigou.orgId in [x["orgId"] for x in self.student.data["data"]["orgRelList"]]
