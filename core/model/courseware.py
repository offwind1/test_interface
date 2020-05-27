import random

url = "http://images.mizholdings.com/"

resources = [
    ["动图.gif", "7", url + "dongtu.gif"],
    ["压缩包.rar", "14", url + "yasuobao.rar"],
    ["压缩包.zip", "14", url + "yasuobao.zip"],
    ["图片.jpg", "7", url + "tupian.jpg"],
    ["图片.png", "7", url + "tupian.png"],
    ["声音.mp3", "12", url + "shengying.mp3"],
    ["文档.doc", "9", url + "wendang.doc"],
    ["文档.docx", "9", url + "wendang.docx"],
    ["演示文稿.ppt", "9", url + "yanshiwendang.ppt"],
    ["演示文稿.pptx", "9", url + "yanshiwendang.pptx"],
    ["表格.xls", "9", url + "biaoge.xls"],
    ["表格.xlsx", "9", url + "biaoge.xlsx"],
    ["视频.flv", "3", url + "shiping.flv"],
    ["视频.mov", "3", url + "shiping.mov"],
    ["视频.mp4", "3", url + "shiping.mp4"],
    ["文档.pdf", "13", url + "wendang.pdf"],
]


class Courseware():
    face_img = "http://images.mizholdings.com/DPMIt6inrH3L~w9g.png"

    def __init__(self, coursewareName, coursewareType, sourceUrl):
        self.courseware_name = coursewareName
        self.courseware_type = coursewareType
        self.source_url = sourceUrl

    @staticmethod
    def random():
        return Courseware(*random.choice(resources))

    @staticmethod
    def jpg():
        return Courseware._find("jpg")

    @staticmethod
    def gif():
        return Courseware._find("gif")

    @staticmethod
    def png():
        return Courseware._find("png")

    @staticmethod
    def mp3():
        return Courseware._find("mp3")

    @staticmethod
    def ppt():
        return Courseware._find("ppt")

    @staticmethod
    def pptx():
        return Courseware._find("pptx")

    @staticmethod
    def flv():
        return Courseware._find("flv")

    @staticmethod
    def mov():
        return Courseware._find("mov")

    @staticmethod
    def mp4():
        return Courseware._find("mp4")

    @staticmethod
    def pdf():
        return Courseware._find("pdf")

    @staticmethod
    def _find(key):
        for name, type, url in resources:
            if name.endswith(key):
                if "ppt" in key:
                    type = "2"
                return Courseware(name, type, url)
        raise Exception("未找到")
