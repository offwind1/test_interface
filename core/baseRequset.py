import requests
import json as json_package

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
    print(log.format(*args))


class BaseRequest():

    def __init__(self, base_url=None, api=None, name=None):
        self.api = api
        self.base_url = base_url
        self.name = name

    def __getattr__(self, item):
        self.api = item
        return self

    def __call__(self, *args, **kwargs):
        return self

    def post(self, data=None, json=None, **kwargs):
        print_log(POST_LOG,
                  self.url or "",
                  self.name or "未定义",
                  data or "无",
                  json or "无")
        has_headers_print(kwargs)

        res = requests.post(url=self.url, data=data, json=json, **kwargs)
        print_response(res)
        return res

    def get(self, url, params=None, **kwargs):
        print_log(GET_LOG,
                  self.url or "",
                  self.name or "未定义",
                  params or "无")
        has_headers_print(kwargs)
        res = requests.get(url, params=params, **kwargs)
        print_response(res)

        return res

    @property
    def url(self):
        return self.base_url + self.api

    def __str__(self):
        return "<BaseRequest: url:" + self.url
