from .user import *


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
        assertPass(json)
        return json

    @property
    def token(self):
        return self.data["data"]["token"]

    @property
    def userId(self):
        return str(self.data['data']["userId"])

    @property
    def nickname(self):
        return self.data['data']['nickname']

    def new(self, account=None, password=None):
        if account is None:
            account = "test"+"".join(random.sample("123456789", 6))
        if password is None:
            password = "111111"
        data = {
            "account": account,
            "password": password,
            "safeQuesId": 1,
            "quesAnswer": 111111,
            "platform": 3,
        }

        res = Mizhu.api_mobile_userRegister().post(data)
        assertPass(res)
        self.data = self.dynamic_login(account, password)
        return self
