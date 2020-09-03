from core import *


class TestD(TestCase):

    def test_Add(self):
        jigou = Jigou.of("yjq").default()
        lesson = Lesson.creat(jigou, lessonName="助教测试0035")
        lesson.set_teacher("4486398101015552")
        lesson.set_support_teacher(
            "4486398102031360,4486398103063552,4486398104079360,4486398105111552")

        lesson.add_class("1101")
        lesson.applied()

        #湿哒哒

        lesson.add_classroom()



