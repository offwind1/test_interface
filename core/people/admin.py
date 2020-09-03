from .user import *
from ..util import *

class Admin(User):
    def dynamic_login(self, account, password):
        data = {
            "userName": account,
            "password": password
        }
        res = Manage.web_usr_manageLogin().post(data=data)
        json = res.json()
        assertPass(json)
        return json

    @property
    def token(self):
        return self.data["token"]
