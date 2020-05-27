from .execl import *


class TeacherExecl(Execl):
    headers = ["班级名称", "年级", "教师姓名", "任教学科", "教师手机号"]

    def __init__(self):
        super().__init__()
        self.write([self.headers])

    def add_teacher_default(self, config_name):
        config = ConfigReader.m2(config_name)
        for line in config.teacher_execl:
            # self.add(*[line[key] for key in self.headers])
            self.add(*list(line.values()))
