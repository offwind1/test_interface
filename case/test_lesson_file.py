from core import *


class TestLessonFile(TestCase):
    pass

    def test_01(self):
        # 上传课件

        jigou = Jigou.of("yjq").default()
        lesson = Lesson.getOne(jigou)

        json = Mizhu.api_course_uploadFile2().post({
            "sourceUrl": "http://images.mizholdings.com/SmkXFRqsBBuW8tm8.png",
            "faceImg": "http://images.mizholdings.com/DPMIt6inrH3L~w9g.png",
            "lessonId": lesson.lessonId,
            "classroomId": lesson[0].classroomId,
            "coursewareType": 7,
            "coursewareName": "图片",
            "md5": "e4b418d66704b1ced1011f6648fb6b10",
            "token": jigou.token
        }).json()
        assertPass(json)
        coursewareId = json["data"]["coursewareId"]
        coursewareName = json["data"]["coursewareName"]

        # 查看课件
        json = Mizhu.web_classroom_classroomOption().post({
            "token": jigou.token,
            "classroomId": lesson[0].classroomId
        }).json()
        assert_list_has(json["data"]["coursewareList"], "coursewareId", coursewareId)
        assert_list_has(json["data"]["coursewareList"], "coursewareName", coursewareName)

        # 删除课件

        # 查看课件
