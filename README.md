# 2020-5-27更新

## 批量添加教师  
```python
from core import TeacherExecl, Kaca

#创建教师excel模板
teacher_execl = TeacherExecl()
# 单行添加：     "班级名称", "年级", "教师姓名", "任教学科", "教师手机号"
teacher_execl.creat("2年1班", "七年级", "王老师", "数学", "17727272727")
teacher_execl.creat("2年1班", "七年级", "赵老师", "语文", "17711111111")
# 保存文件到本地
teacher_execl.save("教师模板.xls")

# 批量添加教师
Kaca.school_class_manage_creat_excel().post({
    "schoolId": "8628",
    "year": "2020",
}, files={"excelFile":teacher_execl.byte()})

```

#### 使用默认数据创建excel

```yaml
# 按照模板添加，需设置yml文件如下
# yjq.yml
  teacher_execl:
    - 班级名称: ""
      年级: ""
      教师姓名: 教师001
      任教学科: 语文
      教师手机号: "18000000001"
    - 班级名称: ""
      年级: ""
      教师姓名: 教师002
      任教学科: 语文
      教师手机号: "18000000002"
    - 班级名称: ""
      年级: ""
      教师姓名: 教师003
      任教学科: 语文
      教师手机号: "18000000003"
```
```python
from core import TeacherExecl, Kaca

# 创建教师excel模板
teacher_execl = TeacherExecl()
# 使用默认的版本添加
teacher_execl.add_teacher_default("yjq")
# 批量添加教师
Kaca.school_class_manage_creat_excel().post({
    "schoolId": "8628",
    "year": "2020",
}, files={"excelFile":teacher_execl.byte()})

```

## 批量导入学生
```python
from core import *
# 创建学生excel
student_execl = StudentExecl()
# 单行添加学生: "姓名", "账号", "密码", "手机号", "学校", "年级", "班级", "级数"
student_execl.creat("学生001", "student001", "111111", "19200000000")
student_execl.creat("学生002", "student002", "111111") # 省略的部分默认为空

#批量导入学生
jigou = Jigou.of("yjq").default() # 机构用户登录
cla = Clazz.creat(Jigou) # 新建班级

res = Mizhu.web_lesson_uploadFile().post({ #上传学生模板
    "token": jigou.token
}, files={"upfile":student_execl.byte()})
json = res.json()
assertPass(json)
fileName = json["data"]["fileName"] # 获取filename

res = Mizhu.web_lesson_joinClassByFile().post({ # 根据导入文件加入班级
    "token": jigou.token,
    "stuId": cla.classId,
    "fileName": fileName
})
assertPass(res)
```

#### 使用默认数据创建excel
```yaml
# yjq.yml
  student_execl:
    - 姓名: "学生001"
      账号: "baby001"
      密码: "111111"
    - 姓名: "学生002"
      账号: "baby002"
      密码: "111111"
    - 姓名: "学生003"
      账号: "baby003"
      密码: "111111"
```
```python
from core import *
# 创建学生excel
student_execl = StudentExecl()
# 使用默认数据创建excel
student_execl.add_student_default("yjq")
student_execl.save()
```

#### 使用模板数据创建学生
```python
from core import *
# 创建学生excel
student_execl = StudentExecl()
# 使用默认数据创建excel
# 创建200个学生，姓名为 名称0001~名称0200， 账号为 account0001~account0200
student_execl.add_student_by_format("名称%04d", "account%04d", 200)
student_execl.save()
```
## 导入课程

### 带课时模板导入
```python
from core import *

# 创建excel对象
lesson_execl = LessonHasClassExecl()
# 单行添加数据 "课程名称", "课节名称", "开始日期", "开始时间", "结束时间", "学科", "老师", "手机", "年级", "班级"
lesson_execl.creat('批量新增1-1','课时1','2020-02-01','12:00','13:00','数学','林伟坚','13000000004','高三','三5班')
# 快捷添加数据
# 参数为 手机号 和 课时数量
# 会自动生成课程名称，和课节名称。 开始时间为当前时间，结束时间为1小时后，学科默认 数学， 老师名称为默认（注册过的教师这一项不生效） 
# 手机号需要提供， 年级默认 班级默认
lesson_execl.add_lesson_fast("18717171717", 3)
# 结果如下
# '批量新增ajssjw','课时1','2020-05-27','12:00','13:00','数学','老师','18717171717','高三','三5班'
# '批量新增ajssjw','课时2','2020-05-28','12:00','13:00','数学','老师','18717171717','高三','三5班'
# '批量新增ajssjw','课时3','2020-05-29','12:00','13:00','数学','老师','18717171717','高三','三5班'


# 导入课程
jigou = Jigou.of("yjq").default()
Mizhu.web_lesson_lessonUpfile().post({
    "token":jigou.token,
    "createUserId":jigou.userId,
}, files={"upfile":lesson_execl.byte()})
```

### 不带课时导入
```python
from core import *

# 创建excel对象
lesson_execl = LessonNoClassExecl()
# 单行添加数据 '课程名称', '开始日期', '结束日期', '开始时间', '结束时间', '学科', '老师', '手机', '年级', '班级'
lesson_execl.creat('批量新增1','2020-02-01','2020-02-10','12:00','13:00','数学','林伟坚','13000000004','高三','三5班')
# 快捷添加数据
# 参数为 手机号 和 课时数量
# 会自动生成课程名称，和课节名称。 开始时间为当前时间，结束时间为1小时后，学科默认 数学， 老师名称为默认（注册过的教师这一项不生效） 
# 手机号需要提供， 年级默认 班级默认
lesson_execl.add_lesson_fast("18722222222", 4)
# 结果如下
# '批量新增asdasd','2020-05-27','2020-05-30','12:00','13:00','数学','老师','18722222222','高三','三5班'

# 导入课程
jigou = Jigou.of("yjq").default()
Mizhu.web_lesson_lessonUpfile().post({
    "token":jigou.token,
    "createUserId":jigou.userId,
}, files={"upfile":lesson_execl.byte()})
```

## 上传课件

### 课时安排上传课件
```python
from core import *
# 机构用户登录
jigou = Jigou.of("yjq").default()
# 随机获取一个资源信息
cours = Courseware.random()
# 创建课程
lesson = Lesson.creat(jigou)
# 上传课件
res = Mizhu.api_course_uploadFile2().post({
    "sourceUrl": cours.source_url,
    "faceImage": cours.face_img,
    "lessonId": lesson.lessonId,
    "classroomId": lesson[0].classroomId,
    "coursewareType": cours.courseware_type,
    "coursewareName": cours.courseware_name,
    "token": jigou.token,
})
assertPass(res)
```

### 教学资源管理上传
```python
from core import *
# 机构用户登录
jigou = Jigou.of("yjq").default()
# 获取gif类型的资源
cours = Courseware.gif()
# 上传
Mizhu.api_course_uploadFile().post({
    "coursewareType": cours.courseware_type,
    "sourceUrl": cours.source_url,
    "coursewareName": cours.courseware_name,
    "faceImg": cours.face_img,
    "token": jigou.token,
})

# 上传ppt
cours_ppt =  Courseware.ppt()
Mizhu.api_course_uploadPpt().post({
    "coursewareType": cours_ppt.courseware_type,
    "sourceUrl": cours_ppt.source_url,
    "coursewareName": cours_ppt.courseware_name,
    "faceImg": cours_ppt.face_img,
    "token": jigou.token
})

```


## 课程和课时 封装 

```python
from core import *

jigou = Jigou.of("yjq").default()
teacher = Teacher.of("yjq").default()
# 新建课程
# 课程名称默认，课程时间当天，默认一节课
lesson = Lesson.creat(jigou)
lesson = Lesson.creat(jigou, lessonName="课程名称", 
                            classroomCount=4,
                            startTime="2020-05-27 12:00:00",
                            lessonTerm=1,
                            lessonTypeId=1,
                            lessonTag="",
                            lessRemark="",
                            ...)

# 编辑课程
lesson.edit(lessonName="修改名称", classroomCount=5, ...)
# 添加班级
lesson.add_class("844") #班级id
# 添加学生
lesson.add_student(
    "7289997722882", # 学生userId
    "844"   # 班级id,可不填 
)
# 批量设置课时主讲
lesson.set_teacher(teacher.userId) #教师id
# 批量设置助教老师
lesson.set_support_teacher(teacher.userId)# 助教老师id，多个使用逗号分开

# 获取课程id
lesson.lessonId
# 获取课程名称
lesson.lessonName


# 获取课节
classroom = lesson[0] # 获取课时1
classroom = lesson[1] # 获取课时2

# 编辑课件
classroom.edit(classroomName="课时名称", startTime="2020-05-27 12:00:00")

# 设置教师
classroom.set_teacher(teacher.userId)
# 设置助教
classroom.set_support_teacher(teacher.userId)
```




## 班级封装
```python
from core import *
jigou = Jigou.of("yjq").default()
teacher = Teacher.of("yjq").default()

# 新建班级
# 班级名称随机, 默认年级1年级
cls = Clazz.creat(jigou)
# 新建班级，并且指定数据
cls = Clazz.creat(jigou, gradeId="7", className="班级名称")

# 通过班级名称，查找班级
cls = Clazz.findClass(jigou, "机器人专用")

# 通过 id 添加学生
cls.add_student("123123,123123") # userId 可以躲过，使用逗号分开

# 通过 execl 添加学生
student_execl = StudentExecl()
student_execl.add_student_default("yjq")
cls.add_student_by_execl(student_execl)

# 获取id
cls.classId
# 获取学生数量
cls.studentCount
#获取班级名称
cls.className


```




















# 2020-05-18更新

### 新增个人配置文件和便捷式初始化token功能

新增文件夹config,在该目录下新增配置文件  
config.yml文件为项目整体配置文件 
其他yml文件为个人配置文件  
例如yjq.yml为杨工专用的用户信息配置文件 


通过配置文件的设置，可以在代码中方便的获取用户token  


#### 获取默认账号
```yaml
t: #测试服务器
  teacher: #教师属性
    account: teacher003 #默认账号和密码
    password: 111111 
```
```python
teacher = Teacher.of("yjq").default()
print(teacher.token)
print(teacher.account) # teacher003
print(teacher.password) # 111111
```

#### 获取随机账号
```yaml
t: #测试服务器
  teacher: #教师属性
    list: #用于随机
      - account: 18767126032
        password: 111111
      - account: robot0001
        password: 111111
```
```python
teacher = Teacher.of("yjq").random()
print(teacher.token)
print(teacher.account) # 18767126032 or robot0001
print(teacher.password) # 111111
```

#### 获取格式化账号
```yaml
t: #测试服务器
  student: #学生
    format: #格式化获取
      - name: account
        value: robot%04d
        start: 0
        end: 200
      - name: password
        value: 111111
```
```python
student = Student.of("yjq").format()
print(student.token)
print(student.account) # robot0001 ~ robot0200
print(student.password) # 111111
```

#### 读取yml文件的必须设置的属性

yml文件中，以下属性必须存在
- student 学生
- teacher 教师
- jigou 机构
- admin 管理员

这些属性，分别可以通过
```python
Student,of("yml文件名").default()
Teacher,of("yml文件名").default()
Jigou,of("yml文件名").default()
Admin,of("yml文件名").default()
```
方式进行登录并获取token  
也可以通过指定账户密码的方式  
```python
student - Student.of("yjq").login("robot0001", "111111")
```

#### 读取yml文件的其他属性方式

yml文件除了设置以上必须的属性，也可以设置额外的属性
例如：
```yaml
t:
  phone: #手机号
    list:
      - 18000000001
      - 18000000002
      - 18000000003
      - 18000000004
      - 18000000005
      - 18000000006
    registered: 16600010000
```
获取属性的方式为
```python
config = ConfigReader.m2("yjq")
phone_0 = config.phone.list._0 # 18000000001
phone_1 = config.phone.list._1 # 18000000002
registered_phone = config.phone.registered # 16600010000
```

### 新增 用例按指定顺序执行

现在使用核心包`core`的`TestCase`执行测试，测试用例的执行顺序，安装代码的书写顺序来执行
```python
from core import TestCase

class Test(TestCase):

    def test_a(self):
        print(1)

    def test_b(self):
        print(2)

    def test_c(self):
        print(3)

"""
执行顺序为
1
2
3
"""

class Test2(TestCase):

    def test_c(self):
        print(3)

    def test_a(self):
        print(1)

    def test_b(self):
        print(2)
"""
执行顺序为
3
1
2
"""
```
> 使用了这个功能后，用例中以 test 开头的方法都不能被其他对象调用！



## OLD

---
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

