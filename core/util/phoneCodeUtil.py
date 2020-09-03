class PhoneCodeUtil():
    LOGIN = 3

    @classmethod
    def get_code(self, phone, type):
        from core import Mizhu
        json = Mizhu.api_mobile_phoneCodeTest().post({
            "phone": phone,
            "type": type
        }).json()
        return json["data"]


# PhoneCodeUtil.get_code("18866670054","3")