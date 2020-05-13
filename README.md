##### 用例编写

新建一个文件，文件名必须以test_开头  
例如 test_login_case.py

然后引入一下包

``` python
from core import Mizhu, Manage
from unittest import TestCase
```

- core为核心包，主要负责接口的调用  
- unittest单元测试工具

然后创建一个类，继承自 TestCase 对象

在这个类里，增加测试方法  
方法名称必须以 test_ 开头。否则无法被 unittest 检索到  
例如: def test_add_func():

```python
"""test_login_case.py"""

from core import Mizhu, Manage
from unittest import TestCase

class SampleExample(TestCase):
    """简单测试"""
    def test_login(self):
        pass
```


这样我们运行项目下面的 main.py 文件  
系统会自动搜到到 test_login_case.py 文件  
并且自动找到继承自 TestCase 的类 SampleExample  
并运行这个类下面以 test_ 开头的所有方法


#### 调用接口

接口调用需要用到 core 包下面的 Mizhu 和 Manage 对象，这两个对象封装了大部分接口  
Mizhu 即 api.mizholdings.com/t//mizhu/ 为开头的后台和前端使用的接口
Manage 即 api.huijudi.cn/t/mizhumanage 为开头的管理员后台的接口


调用接口有两种方式


```python
from core import Mizhu, Manage
from unittest import TestCase

class SampleExample(TestCase):
    """简单测试"""

    def test_login(self):
        """第一种使用类方法"""

        data = {
            "userName": "robot0001",
            "password": "111111"
        }
        res = Mizhu.web_usr_login().post(data=data)

    def test_login2(self):
        """第二种使用"""
        m2 = Mizhu()
        data = {
            "userName": "robot0001",
            "password": "aa"
        }
        res = m2.web_usr_login().post(data=data)
```

两种方法都对接口 `https://api.mizholdings.com/t/mizhu/web/usr/login` 进行了调用
方法名和接口路由一一对应

例如：  
接口 `https://api.huijudi.cn/t/mizhumanage/web/chanAdv/del`  
这个接口是 mizhumanage 服务器的 则使用 Manage 对象
```python
from core import Mizhu, Manage
res = Manage.web_chanAdv_del().post()
# or
m = Manage()
res = m.web_chanAdv_del().post()
```

两种调用方式的区别是，第一种调用方式会验证接口正确性
例如：  
接口： `https://api.mizholdings.com/t/mizhu/web/usr/login222` 是不存在的
使用第一种放到调用
```python
Mizhu.web_usr_login222().post(data=data)
```  
编译器会报错，因为不存在这个接口

而使用第二种调用方式
```python
m2 = Mizhu()
res = m2.web_usr_login().post(data=data)
```
则不会报错。因为第二种放到不会验证接口的正确性


但第二种方式的好处是接口正确性的验证是需要通过更新core包下的 yml文件来进行的
若有时候服务器更新了接口，测试工具的yml没有更新，使用第一种方式是不能调用的。所以临时的调用使用第二种方式


`web_usr_login()` 方法返回的是一个request对象  
可以对这个对象使用 post 或 get 方法

```python
req = Mizhu.web_usr_login()
res = req.post()
# or 
res = req.get()
```

post 和 get 方法的参数，和 requests 的 post、get 方法参数基本一致。除了不用传递url
```python
Mizhu.web_usr_login().post(data=data, json=json, headers=headers)
requests.post(url=url, data=data, json=json, headers=headers)
```

返回值也和 requests 的一样
```python
res = Mizhu.web_usr_login().post(data=data)
res.json()
res.status_code
```

#### 断言

对返回的接口需要进行断言，才能确定用例是否通过

断言语法 `assert 1==2，'报错信息' `

```python
class SampleExample(TestCase):
    def test_login_f(self):
        """登录测试 密码错误"""
        data = {
            "userName": "robot0001",
            "password": "aa"
        }
        res = Mizhu.web_usr_login().post(data=data)
        assert res.json()["code"] == "200" #断言接口返回的code是否是200，若不是则报错
```



其他使用方法，查看case/test_example.py
