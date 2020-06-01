from .baseAgent import DataAgent
from core.util import *
from core import *


class Lesson(DataAgent):

    @staticmethod
    def add(usr: Teacher, lessonName="新建课程" + random_str(), gradeIds="1", lessonTypeId=1, startTime=None,
            tryLook=0, apply=0, lessonTerm=1, faceImg="https://imagess.mizholdings.com/ad/ad2.png",
            classroomCount=1, classTime=60, classroomPrice=0, free=1, lessRemark="<p>8橙云课，提高学习效率8成！现在就加入此课程吧！</p>",
            lessonTag="", studentCount=200, price=1, buyType=0, custRelease=1
            ):
        if startTime is None:
            startTime = getNow()
        else:
            startTime = str_to_date(startTime)

        endTime = getTime(startTime, classroomCount)

        discount = ((classTime / 6) + classroomPrice) * classroomCount

        list = []

        for i in range(classroomCount):
            list.append({
                "interaction": 4,
                "startTime": getTime(startTime, i).strftime(DATE_FORMAT),
                "classroomId": 1,
            })

        classInfo = json.dumps(list)

        data = {
            "gradeIds": gradeIds,
            "gradeNames": getGradeNames(gradeIds),
            "lessonTypeId": lessonTypeId,
            "startTime": startTime.strftime(DATE_FORMAT),
            "endTime": endTime.strftime(DATE_FORMAT),
            "tryLook": tryLook,
            "apply": apply,
            "lessonTerm": lessonTerm,
            "lessonName": lessonName,
            "faceImg": faceImg,
            "classroomCount": classroomCount,
            "classTime": classTime,
            "classroomPrice": classroomPrice,
            "discount": discount,
            "free": free,
            "lessRemark": lessRemark,
            "lessonTag": lessonTag,
            "studentCount": studentCount,
            "classInfo": classInfo,
            "password": "",
            "price": price,
            "buyType": buyType,
            "custRelease": custRelease,
            "token": usr.token,
        }

        res = Mizhu.web_lesson_add().post(data)
        json_ = res.json()
        assertPass(json_)

        return Lesson(json_["data"]["lessonId"], usr=usr)

    @staticmethod
    def random(usr: Teacher):
        res = Mizhu.web_lesson_list().post({
            "token": usr.token,
            "lessonTypeId": "0",
            "currentPage": "1",
            "pageSize": "10",
            "lessonTerm": "0",
            "org": "0",
            "stockType": "0",
            "lessonName": "",
            "recommend": "",
            "pubType": "",
        })
        json_ = res.json()
        assertPass(json_)

        return Lesson(random.choice([x["lessonId"] for x in json_["data"]["list"]]), usr=usr)

    def __init__(self, lessonId, usr):
        super().__init__()
        self.lessonId = lessonId
        self.usr = usr

    def init_data(self):
        data = {
            "lessonId": self.lessonId,
            "token": self.usr.token
        }
        res = Mizhu.web_lesson_getLessonInfoById().post(data)
        json_ = res.json()

        assert json_["code"] == "200"
        return json_["data"]

    def __getitem__(self, item):
        return Lesson.ClassRoom(self.data["classroomList"][item], self.usr)

    def __sizeof__(self):
        return len(self.data["classroomList"])

    def __len__(self):
        return len(self.data["classroomList"])

    @property
    def startTime(self):
        return self.data.get("lessonInfo").get("startTime", "")

    @property
    def endTime(self):
        return self.data.get("lessonInfo").get("endTime", "")

    @property
    def classroomCount(self):
        return self.data.get("lessonInfo").get("classroomCount", 1)

    @property
    def lessonName(self):
        return self.data.get("lessonInfo").get("lessonName", "")

    @property
    def gradeIds(self):
        return self.data.get("lessonInfo").get("gradeIds", "")

    @property
    def gradeNames(self):
        return self.data.get("lessonInfo").get("gradeNames", "")

    @property
    def lessonTypeId(self):
        return self.data.get("lessonInfo").get("lessonTypeId", "")

    @property
    def tryLook(self):
        return self.data.get("lessonInfo").get("tryLook", "")

    @property
    def apply(self):
        return self.data.get("lessonInfo").get("apply", "")

    @property
    def lessonTerm(self):
        return self.data.get("lessonInfo").get("lessonTerm", "")

    @property
    def faceImg(self):
        return self.data.get("lessonInfo").get("faceImg", "")

    @property
    def classTime(self):
        return int(self.data.get("lessonInfo").get("classTime", 0))

    @property
    def classroomPrice(self):
        return self.data.get("lessonInfo").get("classroomPrice", 0)

    @property
    def lessRemark(self):
        return self.data.get("lessonInfo").get("lessRemark", "")

    @property
    def lessonTag(self):
        return self.data.get("lessonInfo").get("lessonTag", "")

    @property
    def studentCount(self):
        return self.data.get("lessonInfo").get("studentCount", "")

    @property
    def price(self):
        return self.data.get("lessonInfo").get("price", "")

    @property
    def buyType(self):
        return self.data.get("lessonInfo").get("buyType", "")

    @property
    def custRelease(self):
        return self.data.get("lessonInfo").get("custRelease", "")

    def applyed(self):
        """
        提交审核
        :return:
        """
        res = Mizhu.web_lesson_apply().post({
            "token": self.usr.token,
            "lessonId": self.lessonId
        })
        assertPass(res)

    def applied(self):
        """
        通过审核
        :return:
        """
        self.applyed()
        admin = Admin.of("yjq").default()
        res = Manage.web_lesson_lessonReply().post({
            "token": admin.token,
            "lessonId": self.lessonId,
            "pubType": "9",
            "pubMsg": ""
        })
        assertPass(res)

    def add_class(self, cls):
        """
        添加班级
        :param cls: 班级id
        :return:
        """
        res = Mizhu.web_lesson_studentByClassId().post({
            "token": self.usr.token,
            "lessonId": self.lessonId,
            "stuId": cls
        })
        assertPass(res)

    def edit(self, lessonName=None, gradeIds=None, lessonTypeId=None, startTime=None,
             tryLook=None, apply=None, lessonTerm=None, faceImg=None,
             classroomCount=None, classTime=None, classroomPrice=None, free=1, lessRemark=None,
             lessonTag=None, studentCount=None, price=None, buyType=None, custRelease=None):
        if classroomCount is None:
            classroomCount = self.classroomCount
        if startTime is None:
            startTime = str_to_date(self.startTime)
            endTime = str_to_date(self.endTime)
        else:
            startTime = str_to_date(startTime)
            endTime = getTime(startTime, classroomCount)
        if lessonName is None:
            lessonName = self.lessonName
        if gradeIds is None:
            gradeIds = self.gradeIds
            gradeNames = self.gradeNames
        else:
            gradeNames = getGradeNames(gradeIds)
        if lessonTypeId is None:
            lessonTypeId = self.lessonTypeId
        if tryLook is None:
            tryLook = self.tryLook
        if apply is None:
            apply = self.apply
        if lessonTerm is None:
            lessonTerm = self.lessonTerm
        if faceImg is None:
            faceImg = self.faceImg
        if classTime is None:
            classTime = self.classTime
        if classroomPrice is None:
            classroomPrice = self.classroomPrice
        if lessRemark is None:
            lessRemark = self.lessRemark
        if lessonTag is None:
            lessonTag = self.lessonTag
        if studentCount is None:
            studentCount = self.studentCount
        if price is None:
            price = self.price
        if buyType is None:
            buyType = self.buyType
        if custRelease is None:
            custRelease = self.custRelease

        discount = ((classTime / 6) + classroomPrice) * classroomCount

        list = []
        le = len(self)
        for i in range(classroomCount):
            if i < le:
                list.append({
                    "interaction": 4,
                    "startTime": getTime(startTime, i).strftime(DATE_FORMAT),
                    "classroomId": self[i].classroomId,
                })
            else:
                list.append({
                    "interaction": 4,
                    "startTime": getTime(startTime, i).strftime(DATE_FORMAT),
                    "classroomId": 1,
                })

        classInfo = json.dumps(list)
        data = {
            "lessonId": self.lessonId,
            "gradeIds": gradeIds,
            "gradeNames": gradeNames,
            "lessonTypeId": lessonTypeId,
            "startTime": startTime.strftime(DATE_FORMAT),
            "endTime": endTime.strftime(DATE_FORMAT),
            "tryLook": tryLook,
            "apply": apply,
            "lessonTerm": lessonTerm,
            "lessonName": lessonName,
            "faceImg": faceImg,
            "classroomCount": classroomCount,
            "classTime": classTime,
            "classroomPrice": classroomPrice,
            "discount": discount,
            "free": free,
            "lessRemark": lessRemark,
            "lessonTag": lessonTag,
            "studentCount": studentCount,
            "classInfo": classInfo,
            "password": "",
            "price": price,
            "buyType": buyType,
            "custRelease": custRelease,
            "token": self.usr.token,
        }
        res = Mizhu.web_lesson_edit().post(data)
        assertPass(res)
        self.update()

    def add_student(self, ids, stuId=""):
        res = Mizhu.web_lesson_addTeacherStudent().post({
            "token": self.usr.token,
            "lessonId": self.lessonId,
            "ids": ids,
            "stuId": stuId,
        })
        assertPass(res)

    def set_teacher(self, teacherId):
        for classroom in self:
            classroom.set_teacher(teacherId)

    def set_support_teacher(self, teacherId):
        classroomIds = ",".join([classroom.classroomId for classroom in self])
        res = Mizhu.web_classroom_setTeacher().post({
            "classroomIds": classroomIds,
            "teacherIds": teacherId,
            "token": self.usr.token
        })
        assertPass(res)

    # =========================================================

    class ClassRoom(DataAgent):

        def __init__(self, data, usr):
            super().__init__()
            self._data = data
            self.usr = usr

        @property
        def startTime(self):
            return self.data.get("startTime", "")

        @property
        def classroomName(self):
            return self.data.get("classroomName", "")

        @property
        def interaction(self):
            return self.data.get("interaction", "")

        @property
        def classroomId(self):
            return self.data.get("classroomId", "")

        @property
        def lessonId(self):
            return self.data.get("lessonId", "")

        @property
        def classroomOrdery(self):
            return self.data.get("classroomOrdery", "")

        @property
        def classroomRemark(self):
            return self.data.get("classroomRemark", "")

        @property
        def teacherId(self):
            return self.data.get("teacherId", "")

        def set_teacher(self, teacherId):
            """
            设置主讲教师
            :param teacherId: 教师id
            :return:
            """
            self.edit(teacherId=teacherId)

        def set_support_teacher(self, teacherIds):
            """
            设置助教老师
            :param teacherIds: 教师id
            :return:
            """
            res = Mizhu.web_classroom_setTeacher().post({
                "classroomIds": self.classroomId,
                "teacherIds": teacherIds,
                "token": self.usr.token
            })
            assertPass(res)

        def edit(self, teacherId=None, classroomName=None, startTime=None, classroomRemark=None):
            """
            编辑课时
            :param teacherId: 修改教师
            :param classroomName: 修改课时名称
            :param startTime: 修改开课时间
            :param classroomRemark: 修改课堂简介
            :return:
            """
            data = {
                "lessonId": self.lessonId,
                "classroomId": self.classroomId,
                "teacherId": teacherId if teacherId else self.teacherId,
                "classroomName": classroomName if classroomName else self.classroomName,
                "interaction": self.interaction,
                "startTime": startTime if startTime else self.startTime,
                "coursewareId": "",
                "classroomRemark": classroomRemark if classroomRemark else self.classroomRemark,
                "timeLong": "0",
                "classroomOrdery": self.classroomOrdery,
                "token": self.usr.token,
            }
            res = Mizhu.web_classroom_edit().post(data)
            assertPass(res)
            self.update()

        def init_data(self):
            for classroom in Lesson(self.lessonId, self.usr):
                if self.classroomId == classroom.classroomId:
                    return classroom.data
