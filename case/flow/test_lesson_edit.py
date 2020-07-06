from core import *


class TestLessonEdit(TestCase):
    jigou = Jigou.of("yjq").default()

    def test_lesson_edit(self):
        lesson = Lesson.creat(self.jigou, classroomCount=3)

        classroom = lesson[0]
        classroom.delete()
        lesson.update()
        assertValueEqule(len(lesson), 2)

        edit_info = {
            "lessonName": "课程名称修改" + random_str(),
            "classroomCount": 4,
            "gradeIds": "1,2,3",
            "startTime": date_to_str(getNow(1, 1)),
            "lessonTypeId": "7",
            "free": 0,
            "custRelease": 3
        }

        lesson.edit(**edit_info)

        assertValueEqule(lesson.lessonName, edit_info["lessonName"])
        assertValueIn(edit_info["gradeIds"], lesson.gradeIds)
        assertValueEqule(lesson.startTime, edit_info["startTime"])
        assertValueEqule(lesson.lessonTypeId, edit_info["lessonTypeId"])
        assertValueEqule(lesson.custRelease, edit_info["custRelease"])

        assertValueEqule(lesson.classroomCount, edit_info["classroomCount"])
        assertValueEqule(len(lesson), edit_info["classroomCount"])

    def test_lesson_add_video(self):
        lesson = Lesson.creat(self.jigou)
        mp4_video_path = "http://images.mizholdings.com/9pfVd_Ha0IhvgjUi.mp4"
        mov_video_path = "http://images.mizholdings.com/shiping.mov"

        def get_video():
            res = Mizhu.web_lesson_getVideo().post({
                "token": self.jigou.token,
                "lessonId": lesson.lessonId
            })
            json = res.json()
            return json

        json = get_video()
        assertPass(json)
        assertValueEqule(len(json["data"]["list"]), 0)

        res = Mizhu.web_classroom_addClassVideo().post({
            "token": self.jigou.token,
            "classroomId": lesson[0].classroomId,
            "videoPath": mp4_video_path,
            "faceImg": "http://images.mizholdings.com/DPMIt6inrH3L~w9g.png"
        })
        assertPass(res)

        json = get_video()
        assertPass(json)
        assertValueEqule(len(json["data"]["list"]), 1)
        data = json["data"]["list"][0]

        assertValueEqule(data["classroomId"], lesson[0].classroomId)
        assertValueEqule(data["videoPath"], mp4_video_path)
        videoId = data["classroomVideoId"]

        res = Mizhu.web_classroom_editClassVideo().post({
            "token": self.jigou.token,
            "classroomId": lesson[0].classroomId,
            "videoId": videoId,
            "videoPath": mov_video_path,
            "faceImg": "http://images.mizholdings.com/DPMIt6inrH3L~w9g.png"
        })
        assertPass(res)

        json = get_video()
        assertPass(json)
        assertValueEqule(len(json["data"]["list"]), 1)
        data = json["data"]["list"][0]

        assertValueEqule(data["classroomId"], lesson[0].classroomId)
        assertValueEqule(data["videoPath"], mov_video_path)
        videoId = data["classroomVideoId"]
