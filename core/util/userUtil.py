from .assertUtil import assertPass


class UserUtil():
    from core.configReader import ConfigReader
    merge_user = ConfigReader.m2("yjq").merge

    @classmethod
    def delete_user(self, user):
        self.delete(user.userId)

    @classmethod
    def delete(self, userId):
        from core import Mizhu

        json = Mizhu.web_usr_accountMerge().post({
            "nickname": self.merge_user.nickname,
            "account": self.merge_user.account,
            "userPhone": self.merge_user.phone,
            "mizhuCoin": self.merge_user.mizhuCoin,
            "mizhuTime": self.merge_user.mizhuTime,
            "integ": "0",
            "oldUserId": userId,
            "newUserId": self.merge_user.userId,
            "token": self.merge_user.userId,
        }).json()
        assertPass(json)

    @classmethod
    def delete_user_by_search(self, phone="", account=""):
        from core import Manage

        if account or phone:
            json = Manage.web_usr_usrManage().post({
                "currentPage": "1",
                "pageSize": "10",
                "phone": phone,
                "account": account,
                "authenResult": "",
                "queryType": "1",
                "token": self.merge_user.userId
            }).json()
            assertPass(json)

            for usr in json["data"]["list"]:
                self.delete(usr["userId"])

    @classmethod
    def delete_user_phone(cls, phone):
        from core import Manage, Admin
        admin = Admin.of("yjq").default()
        json = Manage.web_usr_removeUserPhone().post({
            "phones": phone,
            "token": admin.token
        }).json()

    @classmethod
    def reply_user(self, userId):
        from core import Manage, Admin
        admin = Admin.of("yjq").default()
        json = Manage.web_usr_managerReplyUser().post({
            "token": admin.token,
            "userId": userId
        }).json()
        assertPass(json)
