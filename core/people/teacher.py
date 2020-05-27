from .user import *


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
