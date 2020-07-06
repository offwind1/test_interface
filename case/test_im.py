from core import *


class TestD(TestCase):

    def get_userId(self):
        l = []
        with open("token.txt", "r") as f:
            for x in f.readlines():
                x = x.strip()
                l.append(x)

        return l[:90]

    def add_user(self, userId, token, code):
        json = Mizhu.api_classInfo_classroomCodeAddUser().post({
            "classroomCode": code,
            "userId": userId,
            "token": token,
        }).json()
        assertPass(json)

    def test_1(self):
        teacher = Teacher.of("yjq").default()

        json = Mizhu.api_classInfo_getCode().post({
            "token": teacher.token
        }).json()
        assertPass(json)
        code = json["data"]["classroomCode"]

        json = Mizhu.api_classInfo_quickStart().post({
            "classroomChannel": "1",
            "classroomName": "微课",
            "classroomCode": code,
            "interaction": "4",
            "isopenHeat": "1",
            "anonymous": "2",
            "appId": "dkzp6zxxh",
            "recorded": "1",
            "token": teacher.token,
        }).json()
        assertPass(json)

        classroomId = json["data"]["classroomInfo"]["classroomId"]
        classroomVideoId = json["data"]["classroomVideoId"]
        cloudAccount = json["data"]["classroomInfo"]["teacherCloudeAccount"]

        try:
            for x in self.get_userId():
                userId, token = x.split("\t")
                self.add_user(userId, token, code)
        except:
            print("=" * 10, "加入课堂失败", "=" * 10)
            print("=" * 10, "加入课堂失败", "=" * 10)
            print("=" * 10, "加入课堂失败", "=" * 10)

        json = Mizhu.api_classInfo_classroomEnd().post({
            "classroomId": classroomId,
            "classroomVideoId": classroomVideoId,
            "cloudAccount": cloudAccount,
            "token": teacher.token,
        }).json()
        assertPass(json)
