from core import *


class TestSupportTeacher(TestCase):
    """助教功能相关"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.jigou = Jigou.of("yjq").default()
        cls.main_teacher = Teacher.of("yjq").default()
        cls.support_teacher = Teacher.of("yjq").random()

        cls.lesson = Lesson.creat(cls.jigou)
        cls.lesson.set_teacher(cls.main_teacher.userId)
        cls.lesson.set_support_teacher(cls.support_teacher.userId)
        cls.lesson.applied()

        cls.classroomId = ""
        cls.classroomVideoId = ""
        cls.cloudAccount = ""

    def test_support_teacher(self):
        """助教开课列表中，有这堂课"""
        res = Mizhu.api_classInfo_roomToday().post({
            "token": self.support_teacher.token
        })
        json = res.json()
        assertPass(json)
        assert any([x for x in json["data"] if x["lessonId"] == self.lesson.lessonId])

    def test_support_classroom_start(self):
        """助教开课"""
        json = Mizhu.api_classInfo_classroomStart().post({
            "classroomId": self.lesson[0].classroomId,
            "isopenHeat": "0",
            "vs": "0",
            "recorded": "4",
            "channel": "4",
            "appId": "dl2b1o5dp",
            "token": self.support_teacher.token
        }).json()
        assertPass(json)

        self.classroomId = json["data"]["classroomInfo"]["classroomId"]
        self.classroomVideoId = json["data"]["classroomVideoId"]
        self.cloudAccount = json["data"]["classroomInfo"]["teacherCloudeAccount"]

        """主讲开课"""
        res = Mizhu.api_classInfo_classroomStart().post({
            "classroomId": self.lesson[0].classroomId,
            "isopenHeat": "0",
            "vs": "0",
            "recorded": "4",
            "channel": "4",
            "appId": "dl2b1o5dp",
            "token": self.main_teacher.token
        })
        assertPass(res)

        self.end_classroom(self.support_teacher)
        self.end_classroom(self.main_teacher)

    def test_del_support_teacher(self):
        """删除助教后，开课列表"""
        self.lesson.set_support_teacher(self.main_teacher.userId)
        res = Mizhu.api_classInfo_roomToday().post({
            "token": self.support_teacher.token
        })
        json = res.json()
        assertPass(json)
        assert any([x for x in json["data"] if x["lessonId"] == self.lesson.lessonId]) == False

    def end_classroom(self, usr: Teacher):
        res = Mizhu.api_classInfo_classroomEnd().post({
            "classroomId": self.classroomId,
            "classroomVideoId": self.classroomVideoId,
            "cloudAccount": self.cloudAccount,
            "token": usr.token,
        })
        assertPass(res)
