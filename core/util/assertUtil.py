CODE = ["0", "200"]
RESULT = "0"


def get_list_item(list, key, value):
    v = []
    for x in list:
        if x[key] == value:
            v.append(x)
    return v


def assert_list_has(list, key, value):
    if len(get_list_item(list, key, value)) > 0:
        return
    raise Exception("未找到")


def assert_list_no_has(list, key, value):
    if len(get_list_item(list, key, value)) == 0:
        return

    raise Exception("存在")


def assert_list_has_one(list, key, value):
    le = len(get_list_item(list, key, value))
    if le == 1:
        return
    raise Exception("has {}".format(le))


def assertPass(obj):
    if isinstance(obj, dict):
        assertJsonPass(obj)
    elif isinstance(obj, object) and hasattr(obj, "json"):
        assertJsonPass(obj.json())
    else:
        raise Exception("传入的参数只能是 response 或者 response.json() 对象")


def assertJsonPass(json):
    if "result" in json:
        assertValueEqule(json["result"], RESULT)
    elif "code" in json:
        # assertValueEqule(json["code"], CODE)
        assertValueIn(json["code"], CODE)
    else:
        raise Exception("返回结果中，没有code 也没有 result")


def assertValueIn(a, b):
    assert str(a) in b


def assertValueEqule(a, b):
    assert str(a) == str(b), str(a) + "!=" + str(b)


def assertValueIsNotNull(v):
    assert v


def assertValueIsNull(v):
    assert not v
