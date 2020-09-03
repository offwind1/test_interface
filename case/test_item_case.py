from core import *


class TestItemCase(TestCase):
    jigou = Jigou.of("yjq").default()
    itemId = None
    lessons = None

    def test_item(self):
        """创建项目"""
        lessons = set()
        for i in range(4):
            lesson = Lesson.random(self.jigou)
            lessons.add(lesson.lessonId)

        itemId = self.creat_item(lessons)
        TestItemCase.itemId = itemId
        TestItemCase.lessons = lessons

        self.get_by_id_check(itemId, lessons, None)

    def test_item_update(self):
        """更新项目"""
        prices = [(i * 10, i * 5) for i in range(1, 3)]

        self.update_item(self.itemId, self.lessons, prices)
        self.get_by_id_check(self.itemId, self.lessons, prices)

    def test_kacaList(self):
        """获取咔嚓课程"""
        student = Student.of("yjq").login("robot0001", "111111")
        res = Mizhu.web_item_getKachaListByUser().post({"token": student.token})
        json = res.json()
        assertPass(json)

        assert self.itemId == json["data"]["list"][0]["itemId"]

    def test_del_item(self):
        """删除项目"""
        if self.itemId:
            res = Mizhu.web_item_delete().post({
                "token": self.jigou.token,
                "itemId": self.itemId
            })
            assertPass(res)

    def creat_item(self, lessons):
        """创建项目"""
        lesson_obj = [{
            "lessonId": lesson,
            "required": 1,
            "seq": i,
        } for i, lesson in enumerate(lessons)]

        itemName = "咔嚓" + random_str()
        data = {
            "token": self.jigou.token,
            "itemName": itemName,
            "loginTypes": "2,3",
            "lessonIdJson": obj_2_json_str(lesson_obj),
            "itemDiscountJson": "[]",
            "introduce": "<p>尚禾教育，尚享新智能，禾苗润必舒。</p>",
        }

        res = Mizhu.web_item_add().post(data)
        assertPass(res)

        data = {
            "token": self.jigou.token,
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

    def update_item(self, itemId, lessons, prices):
        """更新项目"""
        lesson_obj = [{
            "lessonId": lesson,
            "required": 1,
            "seq": i,
        } for i, lesson in enumerate(lessons)]

        prices_obj = [{"meetPrice": a, "discountsPrice": b} for a, b in prices]

        itemName = "咔嚓" + random_str()
        data = {
            "itemId": itemId,
            "itemName": itemName,
            "loginTypes": "2,3",
            "lessonIdJson": obj_2_json_str(lesson_obj),
            "itemDiscountJson": obj_2_json_str(prices_obj),
            "introduce": "<p>尚禾教育，尚享新智能，禾苗润必舒。</p>",
            "token": self.jigou.token
        }

        res = Mizhu.web_item_update().post(data)
        assertPass(res)

    def get_by_id_check(self, itemId, lessons, items):
        """断言详情检查"""
        data = {
            "token": self.jigou.token,
            "itemId": itemId
        }
        res = Mizhu.web_item_getById().post(data)
        json = res.json()
        assertPass(json)

        liList = json["data"]["OrgPayitem"]["liList"]
        idList = json["data"]["OrgPayitem"]["idList"]

        if lessons:
            li_set = set([x["lessonId"] for x in liList])
            assert li_set == lessons

        if items:
            id_set = [(x["meetPrice"], x["discountsPrice"]) for x in idList]
            assert id_set == items
