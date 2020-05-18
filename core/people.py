from core import *


class User:
    _user_cache = {}

    def __init__(self, config, cache_key):
        self._congig = config
        self._cache_key = cache_key
        if cache_key not in self._user_cache:
            self._user_cache[cache_key] = {}

    def key(self):
        return self.__class__.__name__

    @classmethod
    def of(cls, config_name):
        config = ConfigReader.m2(config_name)
        return cls(config, config_name.split(".")[0])

    def default(self, refresh=False):
        """
        获取默认的用户，使用缓存，全局只请求一次
        refresh 刷新，强行更新缓存
        """
        class_name = self._get_class_name()
        if refresh or self._user_cache.get(self._cache_key, {}).get(class_name, None) is None:
            user_data = getattr(self._congig, class_name)
            self.data = self._login(user_data.account, user_data.password)
            self._user_cache[self._cache_key][class_name] = self
        return self._user_cache[self._cache_key].get(class_name)

    def random(self):
        """随机获取默认的用户，不进行缓存，每次调用都请求一次"""
        class_name = self._get_class_name()
        user_data = getattr(self._congig, class_name)
        user_data = user_data.random
        self.data = self._login(user_data.account, user_data.password)
        return self

    def format(self):
        class_name = self._get_class_name()
        user_data = getattr(self._congig, class_name)
        user_data = user_data.format
        self.data = self._login(user_data.account, user_data.password)
        return self

    def login(self, account, password):
        self.data = self._login(account, password)
        return self

    def _login(self, account, password):
        self.account = account
        self.password = password
        return self.dynamic_login(account, password)

    def _get_class_name(self):
        return self.__class__.__name__.lower()

    def __str__(self):
        return "<{}: (account:{})>".format(self.__class__.__name__, self.account)


class Student(User):

    def dynamic_login(self, account, password):
        data = {
            "account": account,
            "password": password,
            "longitude": "",
            "latitude": "",
            "phone": "",
            "verifycode": "",
            "machine": "",
        }
        res = Mizhu.api_mobile_login().post(data)
        json = res.json()
        assert json["result"] == 0
        return json

    @property
    def token(self):
        return self.data["data"]["token"]

    @property
    def userId(self):
        return self.data['data']["userId"]

    @property
    def nickname(self):
        return self.data['data']['nickname']


class Teacher(User):
    def dynamic_login(self, account, password):
        data = {
            "userName": account,
            "password": password
        }
        res = Mizhu.web_usr_login().post(data=data)
        json = res.json()
        assert json["code"] == "200"
        return json

    @property
    def token(self):
        return self.data["token"]

    @property
    def userId(self):
        return self.data['data']["userId"]


class Jigou(Teacher):

    @property
    def orgId(self):
        return self.data["data"]["orgId"]

    @property
    def orgName(self):
        return self.data['data']['orgName']


class Admin(User):
    def dynamic_login(self, account, password):
        data = {
            "userName": account,
            "password": password
        }
        res = Manage.web_usr_manageLogin().post(data=data)
        json = res.json()
        assert json["code"] == "200"
        return json

    @property
    def token(self):
        return self.data["token"]
