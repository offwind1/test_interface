from core import *
import copy
import ddt


def update(dict, update):
    dict.update(update)
    return dict


@ddt.ddt
class TestUsrCase(TestCase):
    """usr 接口"""
    config = ConfigReader.m2("yjq")
    jigou = Jigou.of("yjq").default()

    @ddt.unpack
    @ddt.data(
        [{  # "手机号登录",
            "userName": config.phone.registered,
            "password": "111111"}, {
            "code": "200",
            "msg": "登录成功!"
        }],
        [{  # "未注册手机号登录",
            "userName": config.phone.unregistered,
            "password": "111111"}, {
            "code": "300",
            "msg": "账号或密码错误!"
        }],
        [{  # "账号登录",
            "userName": config.teacher.account,
            "password": config.teacher.password}, {
            "code": "200",
            "msg": "登录成功!"
        }],
        [{  # 账号登录密码错误
            "userName": config.teacher.account,
            "password": "123456"}, {
            "code": "300",
            "msg": "账号或密码错误!"
        }],
        [{  # 带有isTeacher登录
            "userName": config.teacher.account,
            "password": "111111",
            "lon": "0",
            "lat": "0",
            "orgId": "1009",
            "isTeacher": "true"
        }, {
            "code": "300",
            "msg": "仅限七檬机构教师登录!"
        }],
        [{  # 异常登录
            "userName": "",
            "password": "12",
        }, {
            "code": "300",
            "msg": "账号或密码错误!"
        }],
        [{  # 邮箱登录
            "userName": config.email.account,
            "password": config.email.password,
        }, {
            "code": "200",
            "msg": "登录成功!"
        }],
        [{  # 账号是手机号，但是数据库里存的是account字段
            "userName": config.phonee_account.account,
            "password": config.phonee_account.password,
        }, {
            "code": "200",
            "msg": "登录成功!"
        }],
    )
    def test_web_usrLogin(self, req, data):
        res = Mizhu.web_usr_login().post(data=req)
        assert res.json()["code"] == data["code"]
        assert res.json()["msg"] == data["msg"]

    delete_user = Student.of("yjq").login(config.temp.phone, config.temp.password)

    @ddt.unpack
    @ddt.data([
        {  # 删除学生
            "orgId": jigou.orgId,
            "teacherId": delete_user.userId,
            "deleteType": "1",
            "token": jigou.token
        }, {
            "code": "200",
            "msg": ""
        },
        Mizhu.web_orgInfo_addStudentToOrg(),
        {
            "account": delete_user.account,
            "orgId": jigou.orgId,
            "token": jigou.token
        }
    ], [
        {  # 删除教师
            "orgId": jigou.orgId,
            "teacherId": delete_user.userId,
            "deleteType": "2",
            "token": jigou.token
        }, {
            "code": "200",
            "msg": ""
        },
        Mizhu.web_orgInfo_addTeacher(),
        {
            "phone": delete_user.account,
            "nickname": delete_user.nickname,
            "userId": delete_user.userId,
            "orgId": jigou.orgId,
            "signIn": "1",
            "token": jigou.token
        }
    ], [
        {  # teacherId 为空
            "orgId": jigou.orgId,
            "teacherId": "",
            "deleteType": "2",
            "token": jigou.token
        }, {
            "code": "300",
            "msg": "token无效"
        },
        None,
        None
    ])
    def test_orgDelTeacher(self, req, data, func, func_req):
        """orgDelTeacher"""
        if func is not None:
            res = func.post(func_req)
            assertPass(res)

        res = Mizhu.web_usr_orgDelTeacher().post(req)
        assert res.json()["code"] == data["code"]
        assert res.json()["msg"] == data["msg"]

    edit_req = {
        "token": "",
        "userId": "",
        "userIdentity": "",
        "userType": "",
        "password": "",
        "photoPath": "",
        "nickname": "",
        "sex": "",
        "age": "",
        "qq": "",
        "context": "",
        "mySign": "",
        "department": "",
        "gradeName": "",
        "className": "",
        "status": "",
        "linkName": "",
        "billPhone": "",
        "address": "",
    }

    merge_info = config.merge
    merge_student = Student.of("yjq").merge()

    @ddt.unpack
    @ddt.data([{
        "nickname": merge_info.nickname,
        "account": merge_info.account,
        "userPhone": merge_info.phone,
        "mizhuCoins": merge_info.mizhuCoin,
        "mizhuTime": merge_info.mizhuTime,
        "integ": "0",
        "oldUserId": merge_student.userId,
        "newUserId": "",
        "token": jigou.token,
    }, {
        "code": "200",
        "msg": "合并成功!",
    },
        True
    ], [{
        "nickname": merge_info.nickname,
        "account": "",
        "userPhone": merge_info.phone,
        "mizhuCoins": merge_info.mizhuCoin,
        "mizhuTime": merge_info.mizhuTime,
        "integ": "0",
        "oldUserId": "111111111",
        "newUserId": "1111111111",
        "token": jigou.token,
    }, {
        "code": "300",
        "msg": "用户未查询到!",
    },
        False
    ], [{
        "nickname": merge_info.nickname,
        "userPhone": merge_info.phone,
        "mizhuCoins": merge_info.mizhuCoin,
        "mizhuTime": merge_info.mizhuTime,
        "integ": "0",
        "oldUserId": "111111111",
        "newUserId": "1111111111",
    }, {
        "code": "300",
        "msg": "token无效，或参数有误!",
    },
        False
    ])
    def test_accountMerge(self, req, data, flag):
        if flag:
            new = Student.of("yjq").new()
            req["newUserId"] = new.userId

        res = Mizhu.web_usr_accountMerge().post(req)
        json = res.json()
        assert json["code"] == data["code"]
        assert json["msg"] == data["msg"]

    student = Student.of("yjq").random()

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "password": student.password
    }, {
        "code": "200",
        "msg": ""
    }], [{
        "token": student.token,
        "password": "aksksksksk"
    }, {
        "code": "300",
        "msg": "密码输入错误"
    }], [{
        "token": "",
        "password": "111"
    }, {
        "code": "300",
        "msg": "密码输入错误"
    }])
    def test_check_password(self, req, data):
        res = Mizhu.web_usr_checkPassword().post(req)
        json = res.json()
        assert json["code"] == data["code"]
        assert json["msg"] == data["msg"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token
    }, {
        "code": "200",
        "msg": "",
        "account": student.account,
        "userId": student.userId
    }], [{
        "tokne": "CBF424A0-9999-1111-0000-DEE57067ED34"
    }, {
        "code": "300",
        "msg": "token无效!"
    }])
    def test_getInfo(self, req, data):
        res = Mizhu.web_usr_getInfo().post(req)
        json = res.json()
        assert json["code"] == data["code"]
        assert json["msg"] == data["msg"]

        if json["code"] == "200":
            assert json["data"]["userInfo"]["account"] == data["account"]
            assert json["data"]["userInfo"]["userId"] == data["userId"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "nickname": "",
        "orgName": "",
        "userPhone": "",
        "userCode": "",
        "currentPage": "1",
        "pageSize": "10",
    }, {
        "code": "200"
    }], [{
        "token": student.token,
        "nickname": "",
        "userIdentity": "2",
        "authen": "2",
        "agentId": "1",
        "orgName": "",
        "userPhone": "",
        "userCode": "",
        "currentPage": "1",
        "pageSize": "10",
    }, {
        "code": "200"
    }])
    def test_list(self, req, data):
        res = Mizhu.web_usr_list().post(req)
        json = res.json()
        assert json["code"] == data["code"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "userId": student.userId
    }, {
        "code": "200",
        "msg": "",
        "account": student.account,
        "userId": student.userId
    }], [{}, {
        "code": "300",
        "msg": "token无效!"
    }])
    def test_get_user_by_id(self, req, data):
        res = Mizhu.web_usr_getUserById().post(req)
        json = res.json()
        assert json["code"] == data["code"]
        assert json["msg"] == data["msg"]
        if json["code"] == "200":
            assert json["data"]["userInfo"]["account"] == data["account"]
            assert json["data"]["userInfo"]["userId"] == data["userId"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "currentPage": "1",
        "pageSize": "10"}, {
        "code": "200"
    }])
    def test_consum_list(self, req, data):
        res = Mizhu.web_usr_consumList().post(req)
        json = res.json()
        assert json["code"] == data["code"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "currentPage": "1",
        "pageSize": "10"}, {
        "code": "200"
    }])
    def test_transaction(self, req, data):
        res = Mizhu.web_usr_transaction().post(req)
        json = res.json()
        assert json["code"] == data["code"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "userId": student.userId
    }, {
        "code": "200"
    }])
    def test_usr_org_info(self, req, data):
        res = Mizhu.web_usr_usrOrgInfo().post(req)
        json = res.json()
        assert json["code"] == data["code"]

    @ddt.unpack
    @ddt.data([{
        "token": student.token,
        "currentPage": "1",
        "pageSize": "10"}, {
        "code": "200"
    }])
    def test_trans_list(self, req, data):
        res = Mizhu.web_usr_transList().post(req)
        json = res.json()
        assert json["code"] == data["code"]
