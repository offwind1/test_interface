from core import *
from core.util.itemFactory import ItemFactory


class TestFreeItem(TestCase):

    # 免费测试项目
    def test_001(self):
        jigou = Jigou.of("yjq").default()
        lesson1 = Lesson.creat(jigou)
        lesson2 = Lesson.creat(jigou)

        itemId = ItemFactory.creat_item_by_lessons_and_user([lesson1, lesson2], jigou)
        urls = ItemFactory.creat_url(itemId)

        for line in urls:
            print(line)
