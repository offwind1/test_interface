import requests
import json as json_package
from core.util.secretUtil import get_sign

URL_LOG = """
url: {} 
接口名称: {}"""

POST_LOG = URL_LOG + """
body: {}
json: {}"""

HEADERS_LOG = """
headers: {}"""

GET_LOG = URL_LOG + """
params: {}"""

RESPONSE_LOG = """
response: {}"""


def has_headers_print(kwargs):
    headers = kwargs.get("headers")
    if headers:
        print(HEADERS_LOG.format(headers))


def print_response(res):
    if res.status_code != 200:
        raise Exception("接口响应返回: {} \n {}".format(res.status_code, res.text))

    try:
        response_json = res.json()
        print_log(RESPONSE_LOG, json_package.dumps(response_json, indent=4, ensure_ascii=False))
    except:
        print(res.text)


def print_log(log, *args):
    args_ = []
    for l in args:
        if isinstance(l, dict):
            args_.append(json_package.dumps(l, indent=4, ensure_ascii=False))
        else:
            args_.append(l)
    print(log.format(*args_))


# 基础请求类
class BaseRequest():

    def __init__(self, base_url=None, api=None, name=None):
        self.api = api # 接口 url
        self.base_url = base_url # 服务器域名
        self.name = name # 接口名称

    def __getattr__(self, item):
        self.api = item
        return self

    def __call__(self, *args, **kwargs):
        return self

    def _secure(self, data, kwargs):
        """
            若接口 url以 api开头 需要进行加密
        """

        if not self.api.startswith("api"):
            return

        # 获取加密后的秘钥
        value = get_sign(data)
        if "headers" not in kwargs:
            kwargs["headers"] = {}

        # 添加到headers中
        kwargs["headers"].update({
            "mizhu": value
        })

    def post(self, data=None, json=None, **kwargs):
        # 打印接口详情
        print_log(POST_LOG,
                  self.url or "",
                  self.name or "未定义",
                  data or "无",
                  json or "无")

        # 加密
        self._secure(data, kwargs)
        # 打印headers
        has_headers_print(kwargs)
        # 调用接口
        res = requests.post(url=self.url, data=data, json=json, **kwargs)
        # 打印response
        print_response(res)
        return res

    def get(self, params=None, **kwargs):
        # 打印接口详情
        print_log(GET_LOG,
                  self.url or "",
                  self.name or "未定义",
                  params or "无")

        # 加密
        self._secure(params, kwargs)
        # 打印headers
        has_headers_print(kwargs)
        # 调用接口
        res = requests.get(self.url, params=params, **kwargs)
        # 打印response
        print_response(res)

        return res

    @property
    def url(self):
        # 域名 和 路由 拼成完整的接口地址
        return self.base_url + self.api

    def __str__(self):
        return "<BaseRequest: url:" + self.url
