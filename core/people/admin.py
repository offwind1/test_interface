from .user import *


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
