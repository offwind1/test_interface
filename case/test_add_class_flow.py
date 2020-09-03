from core import *


class AddClassFlow(TestCase):
    jigou = Jigou.of("yjq").default()

    def test_add_student_by_file(self):
        """通过文件添加学生"""
        cla = Clazz.add(self.jigou)

        # 创建excel
        execl = StudentExecl()
        execl.add_student_by_format("新生娃%04d", "baby%04d", 5)

        self.uploadFile(execl, cla)

        data = {
            "token": self.jigou.token,
            "stuId": cla.classId,
            "currentPage": "1",
            "pageSize": "1"
        }
        res = Mizhu.web_grade_userByStuId().post(data)
        json = res.json()
        assertPass(json)

        for line in json["data"]["list"]:
            assert "新生娃" in line["userName"]
            assert "baby" in line["account"]
            assert "一年级" == line["gradeName"]
            assert cla.classId == line["stuId"]

        self.del_class(cla)

    def test_add_200_student(self):
        """上传超过200条的学生导入文件。检查 接口是否通过，学生数量是否正确"""
        cla = Clazz.add(self.jigou)

        # 创建excel
        execl = StudentExecl()
        execl.add_student_by_format("机器人%04d", "robot%04d", 200)
        self.uploadFile(execl, cla)
        assert cla.studentCount == 200
        self.del_class(cla)

    def uploadFile(self, execl, cla):
        res = Mizhu.web_lesson_uploadFile().post({"token": self.jigou.token}, files={"upfile": execl.byte()})
        json = res.json()
        assertPass(json)
        fileName = json["data"]["fileName"]

        data = {
            "fileName": fileName,
            "stuId": cla.classId,
            "token": self.jigou.token
        }

        res = Mizhu.web_lesson_joinClassByFile().post(data)
        json = res.json()
        assertPass(json)

    def del_class(self, cla):
        data = {
            "stuId": cla.classId,
            "token": self.jigou.token}
        res = Mizhu.web_grade_delClass().post(data)
        assertPass(res)
