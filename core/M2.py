from .baseRequset import BaseRequest
from .config import *


class Mizhu(BaseRequest):
    key = "mizhu"
    host = get_server_host(key)

    def __init__(self, api=None, name=None):
        super().__init__(base_url=self.host + self.key + "/", api=api, name=name)


class Manage(BaseRequest):
    key = "mizhumanage"
    host = get_server_host(key)

    def __init__(self, api=None, name=None):
        super().__init__(base_url=self.host + self.key + "/", api=api, name=name)
