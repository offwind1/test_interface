from core import *


class TestAddTeacher(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.teacher = Teacher.of("yjq").random()
        cls.jigou = Jigou.of("yjq").default()

    def test_del_teacher(self):
        json = Mizhu.web_usr_orgTeacherInfo().post({
            "token": self.jigou.token,
            "currentPage": "1",
            "phone": "",
            "name": "",
            "pageSize": "100"
        }).json()
        assertPass(json)
        if get_list_item(json["data"]["list"], "userId", self.teacher.userId):
            json = Mizhu.web_usr_orgDelTeacher().post({
                "token": self.jigou.token,
                "orgId": self.jigou.userId,
                "teacherId": self.teacher.userId,
                "deleteType": "2"
            }).json()
            assertPass(json)

        json = Mizhu.web_usr_orgTeacherInfo().post({
            "token": self.jigou.token,
            "currentPage": "1",
            "phone": "",
            "name": "",
            "pageSize": "100"
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"]["list"], "userId", self.teacher.userId)

    def test_add_teacher_by_file(self):
        # 创建教师excel模板
        teacher_execl = TeacherExecl()
        # 单行添加：     "班级名称", "年级", "教师姓名", "任教学科", "教师手机号"
        teacher_execl.add("2年1班", "七年级", "王老师", "数学", self.teacher.phone)

        # 批量添加教师
        json = Kaca.school_class_manage_creat_excel().post({
            "schoolId": self.jigou.orgId,
            "year": "2020",
        }, files={"excelFile": teacher_execl.byte()}).json()
        assertPass(json)

        json = Mizhu.web_usr_orgTeacherInfo().post({
            "token": self.jigou.token,
            "currentPage": "1",
            "phone": "",
            "name": "",
            "pageSize": "100"
        }).json()
        assertPass(json)
        assert_list_has(json["data"]["list"], "userId", self.teacher.userId)
