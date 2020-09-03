from .user import *
from ..util import *


class Teacher(User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._info = None

    def dynamic_login(self, account, password):
        data = {
            "userName": account,
            "password": password
        }
        res = Mizhu.web_usr_login().post(data=data)
        json = res.json()
        assertPass(json)
        return json

    def _get_teacher_info(self):
        json = Mizhu.api_mobile_userInfo().post({
            "token": self.token
        }).json()
        assertPass(json)

        return json['data']

    @property
    def info(self):
        if self._info is None:
            self._info = self._get_teacher_info()
        return self._info

    @property
    def token(self):
        return self.data["token"]

    @property
    def userId(self):
        return self.data['data']["userId"]

    @property
    def phone(self):
        return self.info['userPhone']
