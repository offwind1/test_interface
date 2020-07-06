from core import *


def get_userId():
    l = []
    with open("token.txt", "r") as f:
        for x in f.readlines():
            x = x.strip()
            l.append(x)

    return l[:20]


class TestD(TestCase):

    def test_Asdd(self):
        jigou = Jigou.of("yjq").default()
        lesson = Lesson.creat(jigou, lessonName="sdsdsdsdsdsd")
        lesson.set_teacher("4486398101015552")
        lesson.set_support_teacher(
            "4486398102031360,4486398103063552")

        lesson.add_class("1101")
        lesson.applied()

    def test_adsdasd(self):
        # 创建excel对象
        lesson_execl = LessonHasClassExecl()
        # 单行添加数据 "课程名称", "课节名称", "开始日期", "开始时间", "结束时间", "学科", "老师", "手机", "年级", "班级"
        lesson_execl.add('批量新增1-1', '课时1', '2020-02-01', '12:00', '13:00', '数学', '林伟坚', '13000000004', '高三', '三5班')
        # 快捷添加数据
        # 参数为 手机号 和 课时数量
        # 会自动生成课程名称，和课节名称。 开始时间为当前时间，结束时间为1小时后，学科默认 数学， 老师名称为默认（注册过的教师这一项不生效）
        # 手机号需要提供， 年级默认 班级默认
        # lesson_execl.add_lesson_fast("18717171717", 3)
        # # 结果如下
        # # '批量新增ajssjw','课时1','2020-05-27','12:00','13:00','数学','老师','18717171717','高三','三5班'
        # # '批量新增ajssjw','课时2','2020-05-28','12:00','13:00','数学','老师','18717171717','高三','三5班'
        # # '批量新增ajssjw','课时3','2020-05-29','12:00','13:00','数学','老师','18717171717','高三','三5班'

        # 导入课程
        jigou = Jigou.of("yjq").default()
        res = Manage.web_lesson_lessonUpfile().post({
            "token": jigou.token,
            "createUserId": jigou.userId,
        }, files={"upfile": lesson_execl.byte()})

        json = res.json()
        batchNum = json["data"]

        Manage.web_lesson_addByfile().post({
            "batchNum": batchNum,
            "orgId": jigou.orgId,
            "createUserId": jigou.userId,
            "token": jigou.token
        })

    def test_vote(self):
        # student = Student.of("yjq").default()

        for x in get_userId():
            userId, token = x.split("\t")

            Mizhu.api_vote_subOption().post({
                "voteId": "c3ffe7a607da4fa1a12be208804185c4",
                "optionIds": "",
                "optionValues": "https://imagess.mizholdings.com/And0e83aeeba079b83a0331c2f1f74ac08b.jpg",
                "token": token
            })
