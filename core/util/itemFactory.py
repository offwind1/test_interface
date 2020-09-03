from core import *


class ItemFactory():

    @staticmethod
    def creat_item_by_lessons_and_user(lessons, user):
        lesson_obj = [{
            "lessonId": lesson.lessonId,
            "required": 1,
            "seq": i,
        } for i, lesson in enumerate(lessons)]

        itemName = "收费项目测试" + random_str()
        sum = 0
        for lesson in lessons:
            sum += lesson.realPrice

        data = {
            "token": user.token,
            "itemName": itemName,
            "loginTypes": "2,3",
            "lessonIdJson": obj_2_json_str(lesson_obj),
            "itemDiscountJson": '[{"meetPrice":"%f","discountsPrice":"%f"}]' % (sum, sum - 0.01),
            "introduce": "<p>尚禾教育，尚享新智能，禾苗润必舒。</p>",
        }
        res = Mizhu.web_item_add().post(data)
        assertPass(res)

        data = {
            "token": user.token,
            "page": "1",
            "pageSize": "100"
        }

        res = Mizhu.web_item_list().post(data)
        json = res.json()
        assertPass(json)

        for line in json["data"]["OrgPayitemList"]:
            if itemName == line["itemName"]:
                return line["itemId"]

        raise Exception("未找到项目")

    base_url = "https://api.mizholdings.com/wxpub/t/newCart?id={}"

    @classmethod
    def creat_url(cls, itemId):
        return [
            cls.a_url(itemId),
            cls.b_url(itemId),
            cls.c_url(itemId),
            cls.school_url(itemId),
        ]

    @classmethod
    def a_url(cls, itemId):
        return cls.url(itemId) + "&state=a"

    @classmethod
    def b_url(cls, itemId):
        return cls.url(itemId) + "&state=b"

    @classmethod
    def c_url(cls, itemId):
        return cls.url(itemId) + "&state=b"

    @classmethod
    def school_url(cls, itemId, school="8773"):
        return cls.url(itemId) + "&state=bc&school={}".format(school)

    @classmethod
    def url(cls, itemId):
        return cls.base_url.format(itemId)
