from core import *


# 课程显示测试


class TestLessonShow(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.jg1 = Jigou.of("yjq").default()
        cls.jg2 = Jigou.of("yjq").random()

        cls.student = Student.of("yjq").login("robot0401", "111111")
        cls.lesson = Lesson.creat(cls.jg1, custRelease=2)
        cls.lesson.applied()

    def test_jigou_lesson_show(self):
        """机构课程，显示在校本课程中"""
        json = self.lesson_list(self.jg1)
        self.assert_has_lesson(json["data"])

    def test_stroe_lesson_show(self):
        """课程库课程，显示在其他机构的课程库中"""
        res = Mizhu.web_lesson_stockList().post({
            "token": self.jg2.token,
            "lessonName": "",
            "lessonTypeId": 0,
            "gradeId": "",
            "orgId": self.jg2.orgId,
            "currentPage": 1,
            "pageSize": 12
        })
        json = res.json()
        assertPass(json)

        self.assert_has_lesson(json["data"]["list"])

    def test_add_stroe_lesson(self):
        """添加课程库课程"""
        res = Mizhu.web_lesson_stockJoin().post({
            "token": self.jg2.token,
            "lessonIds": self.lesson.lessonId,
            "orgId": self.jg2.orgId,
            "applyIds": ""
        })
        assertPass(res)

    def test_my_stock_lesson(self):
        """已选课程中，应该有该课程"""
        res = Mizhu.web_lesson_stockMy().post({
            "token": self.jg2.token,
            "lessonTypeId": 0,
            "gradeId": 0,
            "orgId": self.jg2.orgId,
            "currentPage": 1,
            "pageSize": 12,
        })
        json = res.json()
        assertPass(json)
        self.assert_has_lesson(json["data"]["list"])

    def test_add_stock_jigou_show(self):
        """添加了其他机构的课程库课程，显示在自己的校本课程中"""
        json = self.lesson_list(self.jg2)
        self.assert_has_lesson(json["data"])

    def test_del_my_stock_(self):
        """删除我的课程库的课程"""
        res = Mizhu.web_lesson_stockDel().post({
            "token": self.jg2.token,
            "lessonIds": self.lesson.lessonId,
            "orgId": self.jg2.orgId
        })
        assertPass(res)

    def test_del_show(self):
        """删除课程库后，校本课程中不显示"""
        json = self.lesson_list(self.jg2)
        self.assert_has_lesson(json["data"], flag=False)

    def lesson_list(self, usr: Jigou):
        res = Mizhu.api_lessonInfo_list().post({
            "orgId": usr.orgId,
            "gradeIds": self.lesson.gradeIds.replace(",", ""),
            "token": self.student.token,
            "lessonName": "",
            "page": "1"
        })
        json = res.json()
        assertPass(json)
        return json

    def assert_has_lesson(self, iter, flag=True):
        assert any([x for x in iter if x["lessonId"] == self.lesson.lessonId]) == flag
