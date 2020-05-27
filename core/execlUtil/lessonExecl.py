from .execl import Execl
from ..util import *


class LessonHasClassExecl(Execl):
    headers = ["课程名称", "课节名称", "开始日期", "开始时间", "结束时间", "学科", "老师", "手机", "年级", "班级"]

    def __init__(self):
        super().__init__()
        self.write([self.headers])

    def add_lesson_fast(self, phone: str, count: int):
        list = []
        lesson_name = "批量新增" + random_str()
        for i in range(count):
            date = getNow(i)
            l = [lesson_name,
                 "课时{}".format(i + 1),
                 date.strftime(YMD_DATE_FORMAT),
                 date.strftime(HM_DATE_FORMAT),
                 getNow(i, 1).strftime(HM_DATE_FORMAT),
                 '数学', '老师', phone, '高三', '三5班']
            list.append(l)

        self.write(list)


class LessonNoClassExecl(Execl):
    headers = ['课程名称', '开始日期', '结束日期', '开始时间', '结束时间', '学科', '老师', '手机', '年级', '班级']

    def __init__(self):
        super().__init__()
        self.write([self.headers])

    def add_lesson_fast(self, phone: str, count: int):
        lesson_name = "批量新增" + random_str()
        start = getNow()
        end = getNow(count, 1)
        self.add(*[lesson_name, start.strftime(YMD_DATE_FORMAT), end.strftime(YMD_DATE_FORMAT),
                   start.strftime(HM_DATE_FORMAT), end.strftime(HM_DATE_FORMAT),
                   '数学', '老师', phone, '高三', '三5班'
                   ])
