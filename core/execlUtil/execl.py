import xlsxwriter
from ..configReader import ConfigReader


class Execl:

    def __init__(self, filename="temp.xlsx"):
        self.filename = filename
        self.workbook = xlsxwriter.Workbook(filename)
        self.sheet = self.workbook.add_worksheet("sheet1")
        self.index_row = 0

    def write(self, data):
        for r, row in enumerate(data):
            self.sheet.write_row(self.index_row + r, 0, row)
        self.index_row += r + 1

    def add(self, *args):
        self.write([args])

    def save(self, file_name=None):
        if file_name is not None:
            self.filename = file_name
            self.workbook.filename = file_name
        try:
            self.workbook.close()
        except Exception as e:
            pass

    def byte(self):
        self.save()
        return open(self.filename, "rb")
