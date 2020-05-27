from .execl import *



class StudentExecl(Execl):
    headers = ["姓名", "账号", "密码", "手机号", "学校", "年级", "班级", "级数"]

    def __init__(self):
        super().__init__()
        self.write([self.headers])

    def add_student_by_format(self, nameFormat, accountFormat, count, password="111111"):
        list = []
        for i in range(count):
            row = []
            row.append(nameFormat % i)
            row.append(accountFormat % i)
            row.append(password)
            list.append(row)

        self.write(list)

    def add_student_default(self, config_name):
        config = ConfigReader.m2(config_name)
        for line in config.student_execl:
            self.add(*list(line.values()))
