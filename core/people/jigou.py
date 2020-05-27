from .teacher import Teacher


class Jigou(Teacher):

    @property
    def orgId(self):
        return self.data["data"]["orgId"]

    @property
    def orgName(self):
        return self.data['data']['orgName']
