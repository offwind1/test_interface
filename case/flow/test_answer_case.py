from core import *


class AnswerFlow(TestCase):
    jigou = Jigou.of("yjq").default()
    lesson = Lesson.add(jigou)
    answerCardId = None
    cla = Clazz.findClass(jigou, "答题卡专用")
    lesson.add_class(cla.classId)
    lesson.applied()

    def test_creat_answer(self):
        """创建答题卡"""
        data = self.creat_data(5)
        AnswerFlow.answerCardId = self.creat_answer(data)

        self.check_answer_card(data, self.answerCardId)

    def test_edit_answer(self):
        """修改答题卡"""
        data = self.creat_data(10)
        self.update_answer(data, self.answerCardId)
        self.check_answer_card(data, self.answerCardId)

    def test_student_submit(self):
        """学生提交答题卡"""
        students = []
        for i in range(1, 6):
            student = Student.of("yjq").login("baby%04d" % i, "111111")
            students.append(student)
            self.option_list_check(student, self.answerCardId)
            self.student_answer_card(student, self.answerCardId)

    def test_work_list_check(self):
        """作业模块列表"""
        res = Mizhu.web_answer_getWorkList().post({
            "token": self.jigou.token,
            "lessonId": self.lesson.lessonId
        })
        workList = res.json()
        assertPass(workList)
        o = workList["data"]["laList"][0]

        assertValueEqule(o["answerCardId"], self.answerCardId)
        assertValueEqule(o["studentCount"], 5)

    def test_work_school_list_check(self):
        """提交作业的学校列表"""
        res = Mizhu.web_answer_getWorkSchoolList().post({
            "answerCardId": self.answerCardId,
            "classroomId": self.lesson[0].classroomId,
            "orgId": self.jigou.orgId,
            "token": self.jigou.token
        })
        school = res.json()
        assertPass(school)
        school = school["data"]["oiList"][0]

        assertValueEqule(school["orgId"], self.jigou.orgId)
        assertValueEqule(school["orgName"], self.jigou.orgName)

    def test_work_class_list_check(self):
        """提交作业的班级列表"""
        res = Mizhu.web_answer_getWorkClassList().post({
            "answerCardId": self.answerCardId,
            "classroomId": self.lesson[0].classroomId,
            "orgId": self.jigou.orgId,
            "token": self.jigou.token
        })
        json = res.json()
        assertPass(json)
        json = json["data"]["crList"][0]

        assertValueEqule(json["className"], self.cla.className)
        assertValueEqule(json["classId"], self.cla.classId)

    def test_work_statistics_List_check(self):
        res = Mizhu.web_answer_getWorkStatisticsList().post({
            "answerCardId": self.answerCardId,
            "classroomId": self.lesson[0].classroomId,
            "classId": self.cla.classId,
            "orgId": self.jigou.orgId,
            "token": self.jigou.token
        })
        json = res.json()
        assertPass(json)
        json = json["data"]

        assertValueEqule(json["studentsCount"], 5)
        assertValueEqule(json["notFiled"], 0)

        for i, o in enumerate(json["caList"]):
            assertValueEqule(o["allCount"], 5)

            if i < 4:
                assertValueEqule(o["rightCount"], 5)
            else:
                assertValueEqule(o["rightCount"], 0)

            if i >= 4 and i < 10:
                assertValueEqule(o["wrongCount"], 5)
            else:
                assertValueEqule(o["wrongCount"], 0)
            if i > 9:
                assertValueEqule(o["nullCount"], 5)
                assertValueEqule(o["auto"], 2)
            else:
                assertValueEqule(o["nullCount"], 0)
                assertValueEqule(o["auto"], 1)

    def test_questions_schedule_check(self):
        """答题进度"""
        res = Mizhu.web_answer_getQuestionsSchedule().post({
            "orgId": self.jigou.orgId,
            "classId": self.cla.classId,
            "answerCardId": self.answerCardId,
            "classroomId": self.lesson[0].classroomId,
            "token": self.jigou.token
        })
        assertPass(res)

    def test_edit_answer2(self):
        """答题卡发布后，若有学生提交数据，不能修改"""
        data = self.creat_data(5)
        data["answerCardId"] = self.answerCardId
        res = Mizhu.web_answer_updateAnswerCard().post(data)
        json = res.json()
        assertValueEqule(json["msg"], "已经有学生提交答案，本答题卡不允许修改")

    def test_del_answer(self):
        data = {
            "lessonId": self.lesson.lessonId,
            "classroomId": self.lesson[0].classroomId,
            "answerCardId": self.answerCardId,
            "token": self.jigou.token
        }
        res = Mizhu.web_answer_deleteAnswerCard().post(data)
        assertPass(res)

    # =============================================================

    def creat_data(self, objectiveItemCount=5, subjectiveItemCount=5):
        objectiveItemAnswer_obj = [{
            "answerId": i,
            "questionQtype": "1",
            "realAnswer": chr(65 + i % 4),
        } for i in range(objectiveItemCount)]

        data = {
            "token": self.jigou.token,
            "lessonId": self.lesson.lessonId,
            "classroomId": self.lesson[0].classroomId,
            "objectiveItemCount": objectiveItemCount,
            "subjectiveItemCount": subjectiveItemCount,
            "cardName": "答题卡" + random_str(),
            "objectiveItemAnswer": obj_2_json_str(objectiveItemAnswer_obj)
        }
        return data

    def creat_answer(self, data):
        res = Mizhu.web_answer_addAnswerCard().post(data)
        json = res.json()
        assertPass(json)
        return json["data"]["la"]["answerCardId"]

    def update_answer(self, data, answerId):
        data["answerCardId"] = answerId
        res = Mizhu.web_answer_updateAnswerCard().post(data)
        json = res.json()
        assertPass(json)

    def check_answer_card(self, data, answerId):
        res = Mizhu.web_answer_getAnswerCard().post({
            "lessonId": self.lesson.lessonId,
            "classroomId": self.lesson[0].classroomId,
            "answerCardId": answerId,
            "token": self.jigou.token
        })
        json = res.json()
        assertPass(json)

        answerCard = json["data"]["la"]

        for key in data:
            if key is "token":
                continue
            if key is "objectiveItemAnswer":
                continue
            if key is "subjectiveItemCount":
                continue
            if key is "answerCardId":
                continue

            assertValueEqule(data[key], answerCard[key])

        for i, line in enumerate(answerCard["objectiveItemList"]):
            assert line["realAnswer"] == chr(65 + i % 4)

    def student_answer_card(self, student, answerId):
        student_card_data = self.get_student_card_data(student, answerId)
        answers_list = self.submit_answer_card(student, student_card_data)

    def submit_answer_card(self, student: Student, card_data):
        list = []
        l = []
        for i, line in enumerate(card_data["objectiveItemList"]):
            userAnswer = chr(65 + i)
            list.append({
                "answerId": line["answerId"],
                "userAnswer": userAnswer,
                "answerType": line["answerType"]
            })
            l.append(userAnswer)

        for i, line in enumerate(card_data["subjectiveItemList"]):
            userAnswer = random_str()
            list.append({
                "answerId": line["answerId"],
                "userAnswer": userAnswer,
                "answerType": line["answerType"]
            })
            l.append(userAnswer)

        res = Mizhu.api_answer_submitAnswerCard().post({
            "answerCardId": card_data["answerCardId"],
            "classroomId": card_data["classroomId"],
            "lessonId": card_data["lessonId"],
            "token": student.token,
            "answerListJson": obj_2_json_str(list),
        })
        assertPass(res)

        return l

    def get_student_card_data(self, student: Student, answerId):
        """获取学生答题卡id"""
        res = Mizhu.api_answer_getStudentAnswerCard().post({
            "answerCardId": answerId,
            "lessonId": self.lesson.lessonId,
            "classroomId": self.lesson[0].classroomId,
            "token": student.token
        })
        json = res.json()
        assertPass(json)
        return json["data"]["la"]

    def option_list_check(self, student: Student, answerId):
        """学生课程详情课堂附件查看答题卡"""
        res = Mizhu.api_classInfo_optionList().post({
            "token": student.token,
            "classroomId": self.lesson[0].classroomId
        })
        json = res.json()
        assertPass(json)
        assert json["data"]["laList"][0]["answerCardId"] == answerId
