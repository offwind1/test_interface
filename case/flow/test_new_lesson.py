from core import *


# 课程显示测试


class TestNewLesson(TestCase):
    teacher = Teacher.of("yjq").default()
    student = Student.of("yjq").default()
    jigou = Jigou.of("yjq").default()
    admin = Admin.of("yjq").default()

    def test_1(self):
        """普通用户创建 非课程库课程"""
        lesson = Lesson.creat(self.teacher)
        # 默认不用审核
        assertValueEqule(lesson.pubType, "9")

        # 编辑课程，依旧不用审核
        lesson.edit()
        assertValueEqule(lesson.pubType, "9")

        # 显示在自己的开课列表中
        json = Mizhu.api_classInfo_roomToday().post({
            "token": self.teacher.token
        }).json()

        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)
        # 8橙 app不显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"], "lessonId", lesson.lessonId)

        # 修改为课程库课程
        lesson.edit(custRelease="2")
        # 需要审核
        assertValueEqule(lesson.pubType, "0")
        # 管理员审核通过
        lesson.applied()

        # 显示在自己的开课列表中
        json = Mizhu.api_classInfo_roomToday().post({
            "token": self.teacher.token
        }).json()

        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)
        # 8橙 app不显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        # assert_list_no_has(json["data"], "lessonId", lesson.lessonId)

        # 显示在 管理员的课程库中
        json = Manage.web_lesson_stockList().post({
            "token": self.admin.token,
            "orgId": "0",
            "currentPage": "1",
            "pageSize": "12",
            "lessonName": "",
            "gradeId": "",
            "lessonTypeId": "0",
        }).json()
        assertPass(json)
        assert_list_has(json["data"]["list"], "lessonId", lesson.lessonId)

        # 管理员添加课程库
        json = Manage.web_lesson_stockJoin().post({
            "token": self.admin.token,
            "lessonIds": lesson.lessonId,
            "orgId": "0",
            "applyIds": ""
        }).json()
        assertPass(json)

        # 8橙 app显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

    def test_2(self):
        """机构用户创建，非课程库课程"""
        lesson = Lesson.creat(self.jigou)
        # 不需要审核
        assertValueEqule(lesson.pubType, "9")
        # 显示在自己的开课列表中
        json = Mizhu.api_classInfo_roomToday().post({
            "token": self.jigou.token
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)
        # 8橙 app不显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"], "lessonId", lesson.lessonId)
        # 机构用户 校本课程显示
        json = Mizhu.api_lessonInfo_list().post({
            "orgId": self.jigou.orgId,
            "gradeIds": "1",
            "token": self.student.token,
            "lessonName": "",
            "page": "1"
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

        # 编辑为课程库课程
        lesson.edit(custRelease="2")
        # 需要审核
        assertValueEqule(lesson.pubType, "0")
        # 管理员审核通过
        lesson.applied()
        # 显示在自己的开课列表中
        json = Mizhu.api_classInfo_roomToday().post({
            "token": self.jigou.token
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)
        # 8橙 app不显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"], "lessonId", lesson.lessonId)
        # 机构用户 校本课程显示
        json = Mizhu.api_lessonInfo_list().post({
            "orgId": self.jigou.orgId,
            "gradeIds": "1",
            "token": self.student.token,
            "lessonName": "",
            "page": "1"
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

        # 显示在 管理员的课程库中
        json = Manage.web_lesson_stockList().post({
            "token": self.admin.token,
            "orgId": "0",
            "currentPage": "1",
            "pageSize": "12",
            "lessonName": "",
            "gradeId": "",
            "lessonTypeId": "0",
        }).json()
        assertPass(json)
        assert_list_has(json["data"]["list"], "lessonId", lesson.lessonId)

        # 管理员添加课程库
        json = Manage.web_lesson_stockJoin().post({
            "token": self.admin.token,
            "lessonIds": lesson.lessonId,
            "orgId": "0",
            "applyIds": ""
        }).json()
        assertPass(json)

        # 8橙 app显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

    def test_3(self):
        """机构用户创建 课程库课程"""
        lesson = Lesson.creat(self.jigou, custRelease="2")
        # 默认不用审核
        assertValueEqule(lesson.pubType, "0")
        # 通过审核
        lesson.applied()

        # 显示在 管理员的课程库中
        json = Manage.web_lesson_stockList().post({
            "token": self.admin.token,
            "orgId": "0",
            "currentPage": "1",
            "pageSize": "12",
            "lessonName": "",
            "gradeId": "",
            "lessonTypeId": "0",
        }).json()
        assertPass(json)
        assert_list_has(json["data"]["list"], "lessonId", lesson.lessonId)

        # 管理员添加课程库
        json = Manage.web_lesson_stockJoin().post({
            "token": self.admin.token,
            "lessonIds": lesson.lessonId,
            "orgId": "0",
            "applyIds": ""
        }).json()
        assertPass(json)

        # 8橙 app显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

        # 下架课程
        json = Mizhu.web_lesson_banLesson().post({
            "token": self.jigou.token,
            "lessonId": lesson.lessonId
        }).json()
        assertPass(json)

        lesson.edit(custRelease="1")
        # 通过审核
        lesson.applied()

        # 课程库 已选课程 不存在
        json = Manage.web_lesson_stockMy().post({
            "token": self.admin.token,
            "orgId": "0",
            "currentPage": "1",
            "pageSize": "12",
            "lessonName": "",
            "gradeId": "",
            "lessonTypeId": "0",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"]["list"], "lessonId", lesson.lessonId)

        # 8橙 app不显示
        json = Mizhu.api_top_topMore().post({
            "page": "1",
            "token": self.student.token,
            "orgId": "0",
            "gradeId": "1",
            "topId": "1",
            "hotTop": "1",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"], "lessonId", lesson.lessonId)

    def test_4(self):
        """教师创建课程，转交给机构"""
        lesson = Lesson.creat(self.teacher)

        # 机构列表存在机构
        json = Mizhu.api_org_joinList().post({
            "token": self.teacher.token,
            "isTeacher": "true",
            "page": 0
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "orgId", self.jigou.orgId)

        # 移交
        json = Mizhu.web_lesson_turnOverLesson().post({
            "token": self.teacher.token,
            "lessonIds": lesson.lessonId,
            "type": 1,
            "orgId": self.jigou.orgId,
            "withdraw": "false"
        }).json()
        assertPass(json)

        # 教师 课程列表中 不存在课程
        json = Mizhu.web_lesson_list().post({
            "token": self.teacher.token,
            "lessonName": "",
            "lessonTypeId": "0",
            "pubType": "",
            "recommend": "",
            "currentPage": "1",
            "pageSize": "10",
            "lessonTerm": "0",
            "org": "0",
            "orgId": "0",
            "stockType": "0",
        }).json()
        assertPass(json)
        assert_list_no_has(json["data"]["list"], "lessonId", lesson.lessonId)

        # 机构 课程列表中存在课程
        json = Mizhu.web_lesson_list().post({
            "token": self.jigou.token,
            "lessonName": "",
            "lessonTypeId": "0",
            "pubType": "",
            "recommend": "",
            "currentPage": "1",
            "pageSize": "10",
            "lessonTerm": "0",
            "org": "0",
            "orgId": "0",
            "stockType": "0",
        }).json()
        assertPass(json)
        assert_list_has(json["data"]["list"], "lessonId", lesson.lessonId)
        # 机构用户拥有全部的权限
        x = get_list_item(json["data"]["list"], "lessonId", lesson.lessonId)[0]
        assertValueEqule(x["createUserIdentity"], "1")

        # 机构用户 校本课程显示
        json = Mizhu.api_lessonInfo_list().post({
            "orgId": self.jigou.orgId,
            "gradeIds": "1",
            "token": self.student.token,
            "lessonName": "",
            "page": "1"
        }).json()
        assertPass(json)
        assert_list_has(json["data"], "lessonId", lesson.lessonId)

    def test_05(self):
        """新增课程后，课时序号按照课程开课时间进行重新排序
            使用新增课时接口，加入时间不同的课程。查看最终课时的排序是否正确
        """
        lesson = Lesson.creat(self.teacher)

        a = {
            "classroomName": "a",
            "startTime": date_to_str(getNow(hours=1))
        }

        b = {
            "classroomName": "b",
            "startTime": date_to_str(getNow(day=1))
        }

        c = {
            "classroomName": "c",
            "startTime": date_to_str(getNow(day=1, hours=1))
        }

        lesson.add_classroom(**c)
        lesson.add_classroom(**b)
        lesson.add_classroom(**a)

        x = [x.classroomName for x in lesson]

        assert ["课时1", "a", "b", "c"] == x
