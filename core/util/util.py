import random
import json
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
YMD_DATE_FORMAT = "%Y-%m-%d"
HM_DATE_FORMAT = "%H:%M"


def getGradeNames(gradeIds):
    grade = {
        "": "",
        "1": "一年级",
        "2": "二年级",
        "3": "三年级",
        "4": "四年级",
        "5": "五年级",
        "6": "六年级",
        "7": "七年级",
        "8": "八年级",
        "9": "九年级",
    }

    return ",".join([grade[i] for i in gradeIds.split(",")])


def getNow(day=0, hours=0):
    return datetime.now() + timedelta(days=day, hours=hours)


def getTime(t, day):
    return t + timedelta(days=day)


def str_to_time(str, format):
    return datetime.strptime(str, format)


def str_to_date(str):
    return str_to_time(str, DATE_FORMAT)


def date_to_str(data):
    return data.strftime(DATE_FORMAT)


def random_str(l=6):
    return "".join(random.sample("abcdefghijklmnopqrstuvwxyz", l))


def obj_2_json_str(obj):
    return json.dumps(obj)
