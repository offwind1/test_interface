from core import Jigou, Teacher, Mizhu, Manage, Admin
from core.util import *
from .baseAgent import DataAgent
from ..execlUtil import *


class Clazz(DataAgent):

    @staticmethod
    def add(usr: Jigou, gradeId="1", className="新建班级" + random_str(6), rankNum="2019"):
        data = {
            "token": usr.token,
            "orgName": usr.orgName,
            "orgId": usr.orgId,
            "gradeId": gradeId,
            "gradeName": getGradeNames(gradeId),
            "className": className,
            "rankNum": rankNum,
        }

        res = Mizhu.web_grade_addClass().post(data)
        json_ = res.json()
        assertPass(json_)
        return Clazz(json_["data"]["classId"], usr)

    @staticmethod
    def findClass(usr: Jigou, className):
        res = Mizhu.web_grade_classList().post({
            "token": usr.token,
            "orgName": usr.orgName
        })
        json = res.json()
        assertPass(json)

        for line in json["data"]["list"]:
            if className == line["className"]:
                return Clazz(line["stuId"], usr, data=line)

    def __init__(self, classId, usr, data=None):
        super().__init__()
        self.classId = classId
        self.usr = usr
        if data is not None:
            self.data = data

    def init_data(self):
        data = {
            "token": self.usr.token,
            "orgName": self.usr.orgName
        }
        res = Mizhu.web_grade_classList().post(data)
        json = res.json()
        for line in json["data"]["list"]:
            if line["stuId"] == self.classId:
                return line

        raise Exception("未找到班级")

    @property
    def className(self):
        return self.data["className"]

    @property
    def studentCount(self):
        return self.data["studentCount"]

    def add_student(self, userIds):
        res = Mizhu.web_lesson_joinClassByUserId().post({
            "userIds": userIds,
            "stuId": self.classId,
            "token": self.usr.token
        })
        assertPass(res)

    def add_student_by_execl(self, execl: StudentExecl):
        res = Mizhu.web_lesson_uploadFile().post({  # 上传学生模板
            "token": self.usr.token
        }, files={"upfile": execl.byte()})
        json = res.json()
        assertPass(json)
        fileName = json["data"]["fileName"]  # 获取filename

        res = Mizhu.web_lesson_joinClassByFile().post({  # 根据导入文件加入班级
            "token": self.usr.token,
            "stuId": self.classId,
            "fileName": fileName
        })
        assertPass(res)
