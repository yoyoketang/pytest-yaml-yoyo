# 1 环境与准备

## 1.1 说明

基于 httprunner 框架的用例结构，我自己开发了一个 pytest + yaml 的框架，那么是不是重复造轮子呢？
不可否认 httprunner 框架设计非常优秀，但是也有缺点，httprunner3.x 的版本虽然也是基于 pytest 框架设计，结合 yaml 执行用例，但是会生成一个py文件去执行。
在辅助函数的引用也很局限，只能获取函数的返回值，不能在 yaml 中对返回值重新二次取值。
那么我的这个框架，就是为了解决这些痛点。。。。

本插件可以实现以下优势：

- 1、基于 pytest 框架安装插件即可使用，环境非常简单
- 2、只需要写 yaml 文件用例即可运行，使用 pytest 运行的命令
- 3、extract 功能实现多个接口步骤的参数关联
- 4、全局仅登录一次，在用例中自动在请求头部添加 Authentication token认证
- 5、用例参数化 parameters 功能实现
- 6、yaml 中调用 fixture 功能实现
- 7、yaml 中调用辅助函数功能使用
- 8、yaml 中调用 hooks 功能
- 9、用例分层机制：API和用例层
- 10、支持 logging 日志
- 11、支持 allure 报告
- 12、支持 mysql 数据库增删改查
- 13、支持钉钉机器人通知测试结果和 allure 报告地址
- 14、支持生成随机测试数据，如字符串，姓名，手机号，邮箱等

## 1.2 版本变更记录

v1.0.0
发布的第一个版本（已删除)

v1.0.1  发布时间 2022.11.23
可以安装的第一个版本

- 1.实现基础的 pytest 命令 执行yaml 文件用例功能

v1.0.2 发布时间 2022.11.24

- 1.新增 extract 关键字，在接口中提取返回结果
- 2.参数关联，上一个接口的返回值可以作为下个接口的入参

详细功能参阅 extract 关键字文档

v1.0.3 发布时间 2022.11.28

- 1.config 新增 fixtures 关键字，在yaml 用例中传 fixture 功能和参数化功能
- 2.config 新增 parameters 用例参数化实现

详细功能参阅 parameters 参数化 关键字文档

v1.0.4 发布时间 2022.11.30

hooks 钩子功能实现

- 1.request 钩子对请求参数预处理
- 2.response 钩子对返回结果处理

详细功能参阅 hooks 钩子 关键字文档

v1.0.5 发布时间 2022.12.05

用例分层机制

- 1.API 层对接口的描述，可以复用
- 2.Test case 用例层引用API层

v1.0.6 发布时间 2022.12.06

一个yaml 中写多个用例，用例步骤可以不是list 类型

- 1.config 和 teststeps 不是必须了
- 2.可以自定义用例名称，用例可以是一个步骤也可以是多个步骤


v1.0.7 发布时间 2022.12.08

新增日志

- 1.日志默认按日期时间保存到 logs 目录
- 2.console 日志开启在 pytest.ini 配置，或命令行参数

v1.0.8 发布时间 2022.12.09

结合 allure 生成报告

v1.0.9 发布时间 2022.12.09

全局base_url 配置
- 1.pytest.ini 新增 `base_url` 配置
- 2.命令行新增 `--base-url` 参数

v1.1.0 发布时间 2022.12.13

多环境配置切换
- 1.config.py 实现多环境配置
- 2.pytest.ini 新增 `env` 配置, 命令行新增 `--env` 参数
- 3.支持 mysql 数据库操作
- 4.支持 yaml 中引用 env 环境对象

v1.1.1 发布时间 2022.12.14

钉钉机器人通知测试结果
- 1.config.py 配置钉钉机器人access_token
- 2.测试结果钉钉群通知
- 3.支持 requests_function 和 requests_module 内置 fixture 切换

v1.1.2 发布时间 2022.12.16

内置方法提供
- 1.提供3个常用的内置函数：current_time， rand_value， rand_str
- 2.一个内置fake对象
- 3.修复yaml文件为空或格式不正确时，执行报错的问题

v1.1.3 发布时间 2023.2.13

新增3个关键字
- 1.sleep  添加用例之间的sleep 等待时间
- 2.skip   跳过用例功能
- 3.skipif   条件为真时跳过用例

## 1.3 环境准备

Python 3.8版本
Pytest 7.2.0 最新版

pip 安装插件

```
pip install pytest-yaml-yoyo
```


# 2 快速开始

## 2.1 第一个hello world

yaml 用例编写规则，跟pytest识别默认规则一样，必须是test 开头的，以`.yml` 结尾的文件才会被识别

新建一个`test_hello.yml`文件

```
config:
  name: yy

teststeps:
-
  name: demo
  print: hello world
```

用例整体结构延续了 httprunner 框架的用例结果，主要是为了大家快速上手，减少新的规则学习
- config  是非必须的里面有 name 用例名称，base_url 和 variables 是可选的
- teststeps 是非必须，用例的步骤，用例步骤是一个array 数组类型，可以有多个步骤

从上面的运行可以看出，request 不是必须的，我们可以直接调用python内置函数print 去打印一些内容了。

## 2.2 一个简单的 http 请求

以`http://www.example.com/` get 请求示例
test_get_demo.yml

```
config:
  name: get

teststeps:
-
  name: get
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
```

命令行输入 pytest 后直接运行

```
>pytest
======================= test session starts =======================
platform win32 -- Python 3.8.5, pytest-7.2.0, pluggy-1.0.0
rootdir: D:\demo\yaml_yoyo
plugins: yaml-yoyo-1.0.1
collected 2 items                                                  

test_get_demo.yml .                                          [ 50%]
test_hello.yml .                                             [100%]

======================== 2 passed in 0.49s ========================

```

## 2.3 一个简单的 post 请求

test_post_demo.yml

```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```

## 2.4 validate校验

比如返回的response内容

```
HTTP/1.1 200 OK
Date: Wed, 23 Nov 2022 06:26:25 GMT
Content-Type: application/json
Content-Length: 483
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {}, 
  "data": "{\r\n    \"username\": \"test\",\r\n    \"password\": \"123456\"\r\n}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Content-Length": "55", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "Fiddler", 
    "X-Amzn-Trace-Id": "Root=1-637dbd11-7d9943ba1fb93a9331f6cf8d"
  }, 
  "json": {
    "password": "123456", 
    "username": "test"
  }, 
  "origin": "198.187.30.113", 
  "url": "http://httpbin.org/post"
}

```

校验方式延续了httprunner的校验语法，可以支持response取值对象：status_code, url, ok, headers, cookies, text, json, encoding
其中返回的是json格式，那么可以支持
- jmespath 取值语法: `body.json.username`
- jsonpath 语法: `$..username`
- re 正则语法

如果返回的不是json格式，那么可以用正则取值

## 2.5 变量的声明与引用

变量的声明，只支持在config 声明整个yml文件的全局变量（不支持单个step的变量，减少学习成本）
在 httprunner 里面变量引用语法是`$user`, 引用函数是`${function()}`
我这里统一改成了一个语法变量引用`${var}` 和 引用函数`${function()}` 
（表面上没多大变量，实际上功能强大了很多，使用了强大的jinja2 模板引擎)
可以在引用函数后继续对结果操作， 这就解决了很多人提到了函数返回一个list，如何在yaml中取某一个值的问题

```
config:
  name: post示例
  variables:
    username: test
    password: "123456"

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: ${password}
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```
运行结果
![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a0.png)

# 3 参数关联

## 3.1 extract 提取接口返回参数关联

在自动化用例中，我们经常会看到有人提问，上一个接口的返回的结果，如何取出来给到下个接口的入参。
我们用 extract 关键字提取接口的返回结果（需要更新v1.0.2版本）。

举个例子
用个post请求`http://httpbin.org/post`
```
POST http://httpbin.org/post HTTP/1.1
User-Agent: Fiddler
Host: httpbin.org
Content-Length: 0

HTTP/1.1 200 OK
Date: Thu, 24 Nov 2022 06:18:03 GMT
Content-Type: application/json
Content-Length: 320
Connection: keep-alive
Server: gunicorn/19.9.0
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true

{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Content-Length": "0", 
    "Host": "httpbin.org", 
    "User-Agent": "Fiddler", 
    "X-Amzn-Trace-Id": "Root=1-637f0c9a-23b419f4180f6b843ba941af"
  }, 
  "json": null, 
  "origin": "66.112.216.24", 
  "url": "http://httpbin.org/post"
}
```
比如我需要提取返回接口里面的url参数，那么我们用extract 关键字

test_demo.yml 文件示例
```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]
```

## 3.2 引用提取结果

上一个接口提取到了url 变量，接下来在下个接口中引用`${url}`

```
config:
  name: post示例

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]

-
  name: post
  request:
    method: GET
    url: http://httpbin.org/get
    headers:
      url: ${url}
  validate:
    - eq: [status_code, 200]
```

于是看到请求报文中引用成功
```
GET http://httpbin.org/get HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
url: http://httpbin.org/post

```

## 3.3 extract 提取结果二次取值

我们在上一篇提到**不能在yaml中对返回值重新二次取值。**, 
这也是一些同学提到的问题，对于提取的结果，我想继续取值，比如他是一个字符串，在python中可以用切片取值
那么，在 yaml 中如何实现？

我重新设计的这个框架中，就可以支持python语法，直接用切片取值
```
headers:
      url: ${url[:4]}
```

请求报文
```
GET http://httpbin.org/get HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: keep-alive
url: http

```

**extract 取值语法**

校验方式延续了httprunner的校验语法，可以支持response取值对象：status_code, url, ok, headers, cookies, text, json, encoding
其中返回的是json格式，那么可以支持
- jmespath 语法: body.json.username
- jsonpath 语法: $..username
- re 正则语法：'code: (.+?),'

如果返回的不是json格式，那么可以用正则取值

当一个用例用到多组测试数据的时候，我们必然会用到参数化，接下来看下如何在yaml文件中实现参数化

# 4 全局 Token 管理

我们在使用自动化测试框架的时候，经常会遇到一个需求，希望在全局用例中，仅登录一次，后续所有的用例自动带上请求头部token 或者cookies。

## 4.1 登录fixture 功能

我在 pytest + yaml 框架框架中封装了一个内置 fixture 叫`requests_session`, 它的作用范围是`scope="session"`,也就是全部session用例会话中仅实例化一次。
现在我只需在conftest 中写一个登录的fixture功能，获取token后添加到`requests_session`头部

```
import pytest
import uuid
"""
全局仅登录一次，获取token，
在请求头部添加Authentication Bearer 认证
内置fixture requests_session
"""


def login():
    """登录方法"""
    # 调用登录方法，返回token
    return str(uuid.uuid4())  # noqa


@pytest.fixture(scope="session", autouse=True)
def login_first(requests_session):
    """全局仅一次登录， 更新session请求头部"""
    # 调用登录方法，获得token
    token = login()
    headers = {
        "Authentication": f"Bearer {token}"
    }
    requests_session.headers.update(headers)

```

上面代码中，我用login() 函数实现登录功能，这里返回一个随机值，主要是为了验证我只调用了一次登录方法
接着我写2个yaml文件（**注意，yaml文件中也不需要重复去添加请求头部了**）

test_get_demo.yml
```
config:
  name: get

teststeps:
-
  name: get
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
```

test_post_demo.yml
```
config:
  name: post示例
  variables:
    username: test
    password: "123456"

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: ${password}
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, test]
    - eq: [body.json.username, test]

```

## 4.2 运行用例
在命令行中输入`pytest`运行
抓包看发过去的请求

![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a1.png)
![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a2.png)

于是可以看到，在2个用例中都自动带上了请求头部参数。
（登录cookies的使用原理也是一样的，登录后cookies一般会自动保持）

## 4.3 其它需求

那有些接口不需要登录怎么办呢？比如登录和注册的接口，是不需要带上登录token的，那不能一刀切。
我除了默认用到一个`requests_session` 全局的内置fixture，还预留了2个
-  requests_module:    每个yaml文件中用一次
-  requests_function:  每个用例中用一次

在yaml文件中切换到指定fixture功能，`requests_module` 和 `requests_function` 后续会实现，先实现大需求，解决大部分人遇到的痛点问题！


## 4.4 requests_module 和 requests_function

那有些接口不需要登录怎么办呢？比如登录和注册的接口，是不需要带上登录token的。

除了默认用到一个requests_session 全局的内置fixture，还预留了2个
- requests_module: 每个yaml文件中用一个请求会话（会保持cookies）
- requests_function: 每个用例中用一次，每个用例独立运行，不保持cookies

接下来看下如何在用例中使用test_register.yml

```
config:
  name: post示例
  fixtures: requests_module

注册1:
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test123
      password: "123456"
  validate:
    - eq: [status_code, 200]


注册2:
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test444
      password: "123456"
  validate:
    - eq: [status_code, 200]
```


在config 中传入 fixtures参数，requests_module 是每个yaml文件中用一个请求会话（会保持cookies）
requests_function 作用是每个用例中用一次，每个用例独立运行，不保持cookies。

## 4.5 自定义 fixtures 

pytest 的核心功能是学会灵活使用fixtures， 那么我们的这个插件也是可以支持在用例中调用fixtures功能的。

在conftest.py 文件中写你需要实现的fixture 功能, 设置使用范围为` scope="function" ` 函数级别

```
import pytest


@pytest.fixture(scope="function")
def demo_fixture():
    print("用例前置操作->do something .....")
    yield
    print("用例后置操作，do something .....")

```

在 yaml 文件中引用 fixture 
```
config:
  name: post示例
  fixtures: demo_fixture

注册1:
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test123
      password: "123456"
  validate:
    - eq: [status_code, 200]


注册2:
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test444
      password: "123456"
  validate:
    - eq: [status_code, 200]
```
于是运行结果可以看到，每个用例前后都会执行

```
collected 2 items                                                                                          

test_f2.yml 用例前置操作->do something .....
.用例后置操作，do something .....
用例前置操作->do something .....
用例后置操作，do something .....
```

如果想整个yaml 文件中仅运行一次，那么conftest.py 文件中写你需要实现的 fixture 功能, 设置使用范围为` scope="module" ` 模块级别


```
import pytest


@pytest.fixture(scope="module")
def demo_fixture():
    print("用例前置操作->do something .....")
    yield
    print("用例后置操作，do something .....")

```
于是看到运行的时候，仅在yaml 文件的全部用例中只执行一次
```
collected 2 items                                                                                          

test_f2.yml 用例前置操作->do something .....
..用例后置操作，do something .....
```

## 4.6 多个fixtures的使用

当 yaml 中的用例需要用到多个fixtures时, 支持2种格式

格式一: 逗号隔开
```
config:
  fixtures: fixture_name1,  fixture_name2
```
格式二: 用 list
```
config:
  fixtures: [fixture_name1,  fixture_name2]
```

requests_module 和 requests_function 内置 fixture 功能在 v1.1.1 版本实现， 版本太低的请及时更新版本。


# 5 parameters 参数化

## 5.1 参数化数据结果

当一个用例用到多组测试数据的时候，我们必然会用到参数化，接下来看下如何在yaml文件中实现参数化
用例参数化的实现，我设计了2种实现方式

参数化方式1：
```
  config:
     name: post示例
     fixtures: username, password
     parameters:
       - [test1, '123456']
       - [test2, '123456']
```
参数化方式2：
```
  config:
     name: post示例
     parameters:
       - {"username": "test1", "password": "123456"}
       - {"username": "test2", "password": "1234562"}
```

## 5.2 使用 fixtures 功能实现参数化

基本实现原理参考 pytest 框架的参数化实现
```
import pytest
@pytest.mark.parametrize("test_input,expected",
                         [ ["3+5", 8],
                           ["2+4", 6[,
                           ["6 * 9", 42[,
                         ])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```
在上面的用例中，只需要关注参数化的2个变量test_input, expected 也就是在测试用例中传的2个值，可以理解为用例的2个fixture参数
还需要关注测试数据，测试数据结构必须是list，里面是可以迭代的数据，因为有2个变量，所以每组数据是2个值。

在yaml文件中
- 参数化需要的变量写到 config 的 fixtures 位置
- 参数化需要的数据写到 parameters

示例
test_params.yml
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/

config:
  name: post示例
  fixtures: username, password
  parameters:
    - [test1, '123456']
    - [test2, '123456']

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: ${password}
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, '${username}']
    - eq: [body.json.username, '${username}']
```
运行yaml文件
```
pytest test_params.yml
```
会自动生成2个测试用例
```
(venv) D:\code\tests>pytest test_params.yml
======================== test session starts ========
platform win32 -- Python 3.8.5, pytest-7.2.0, pluggy-1.0.0
rootdir: D:\code\pytest-yaml-yoyo
plugins: yaml-yoyo-1.0.3
collected 2 items                                                                                          

test_params.yml ..                                   [100%]


=================== 2 passed in 0.77s  ================
```


## 5.3 parameters 实现参数化

第二种实现方式，可以在fixtures 中传变量，但是测试数据必须是字典类型，从字典的key中动态读取变量名称
test_params_2.yml
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
config:
  name: post示例
  parameters:
    - {"username": "tes1", "password": "123456"}
    - {"username": "tes2", "password": "123456"}

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: ${password}
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$..username, '${username}']
    - eq: [body.json.username, '${username}']
```

运行yaml文件
```
pytest test_params.yml
```

以上2种实现参数化方式效果是一样的


# 6 yaml 中调用内置方法

pytest-yaml-yoyo 插件使用了强大的jinja2 模板引擎，所以我们在yaml文件中可以写很多python内置的语法了。

## 6.1 调用 python 内置方法
举个例子：
我定义了一个变量username的值是test123，但是我引用变量的时候只想取出前面四个字符串，于是可以用到引用变量语法
```
$(username[:4])
```
可以直接对变量用python的切片语法

test_fun1.yml
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
config:
  name: 引用内置函数
  variables:
    username: test123

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username[:4]}
      password: "123456"
  validate:
    - eq: [status_code, 200]
    - eq: [$..username, test]
```
命令行执行用例
```
pytest test_fun1.yml
```
运行结果
```
POST http://httpbin.org/post HTTP/1.1
Host: httpbin.org
User-Agent: python-requests/2.28.1
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 42
Content-Type: application/json

{"username": "test", "password": "123456"}
```

## 6.2 字典对象取值

如果定义一个字典类型的变量，我们在取值的时候也可以根据key取值
如定义变量
```
  variables:
    username: test123
    body:
      user: yoyo
      email: 123@qq.com
```

user和email的取值用2种方式,通过`点属性`或者用字典取值方法`[key]`
```
      username: ${body.user}
      email: ${body["user"]}
```

test_fun2.yml完整示例
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
config:
  name: 引用内置函数
  variables:
    username: test123
    body:
      user: yoyo
      email: 123@qq.com

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${body.user}
      password: "123456"
      email: ${body["user"]}
  validate:
    - eq: [status_code, 200]
    - eq: [$..username, '${body.user}']
```

# 7 自定义函数功能

一些复杂的逻辑处理，需自己写代码去实现，于是可以自定义函数。

## 7.1 自定义函数

自定义函数的实现，需在conftest.py (pytest 框架内置的插件文件)文件中实现

```
# conftest.py
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/

from pytest_yaml_yoyo import my_builtins
import uuid
import random


def random_user():
    """生成随机账号 4-16位数字+字符a-z"""
    return str(uuid.uuid4()).replace('-', '')[:random.randint(4, 16)]


# 注册到插件内置模块上
my_builtins.random_user = random_user


if __name__ == '__main__':
    print(random_user())
```
实现基本原理是自己定义一个函数，然后注册到插件内置模块 `my_builtins`。这样我们在用例中就能找到该函数方法了

test_fun3.yml 用例中引用内置函数示例
```
config:
  name: 引用内置函数
  variables:
    username: ${random_user()}
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${username}
      password: "123456"
  validate:
    - eq: [status_code, 200]
    - eq: [$..username, '${username}']
```

## 7.2 函数传参数

在引用自定义函数的时候，也可以传变量
```
# conftest.py
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/

from pytest_yaml_yoyo import my_builtins

def func(x):
    return f"hello{x}"


my_builtins.func = func
```

test_fun4.yml示例
```
config:
  name: 引用内置函数
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${func("xxx")}
      password: "123456"
  validate:
    - eq: [status_code, 200]
```

函数还能引用自己在config 中定义的变量

```
config:
  name: 引用内置函数
  variables:
    var: test123
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${func(var)}
      password: "123456"
  validate:
    - eq: [status_code, 200]
```

## 7.3 函数返回的结果也能二次取值

如果一个函数返回list类型，我们在用例中也能取出其中的一个值
```
# conftest.py
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/

from pytest_yaml_yoyo import my_builtins

def func_list():
    return ['test1', 'test2', 'test3']


my_builtins.func_list = func_list
```
test_fun5.yml示例
```
config:
  name: 引用内置函数

teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${func_list().1}
      password: "123456"
  validate:
    - eq: [status_code, 200]
```
list类型支持2种取值方式`${func_list().1}` 或者 `${func_list()[1]}`

## 7.4 内置函数的使用

目前暂时提供了3个内置函数，和1个内置对象
- current_time(f: str = '%Y-%m-%d %H:%M:%S')，  获取当前时间 默认格式为2022-12-16 22:13:00，可以传f参数自定义格式
- rand_value(target: list)   从返回的 list 结果随机取值， 有小伙伴提到的需求
- rand_str(len_start=None, len_end=None)  生成随机字符串，默认32位


还提供了一个内置的fake 对象，可以生成随机手机号，随机身份证，姓名等数据

使用方法:`${fake.name()}`, `fake.phone_number()`, `fake.email()` 等，具体查看Faker模块提供的方法[https://www.cnblogs.com/yoyoketang/p/14869348.html](https://www.cnblogs.com/yoyoketang/p/14869348.html)


current_time() 获取当前时间, 使用示例

```
获取当前时间:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: ${current_time()}
      password: "123456"
  validate:
    - eq: [status_code, 200]

```

rand_value(target: list)   从返回的 list 结果随机取值， 有小伙伴提到的需求
```
提取list值:
-
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      data: ["hello", "world", "hello world"]
  extract:
    res: $.json.data
  validate:
    - eq: [status_code, 200]

随机取一个结果:
-
  request:
    method: GET
    url: http://httpbin.org/get
    params:
      key: ${rand_value(res)}
  validate:
    - eq: [status_code, 200]
```


rand_str(len_start=None, len_end=None)  生成随机字符串，默认32位

rand_str 使用方法：
${rand_str()}  得到32位字符串
${rand_str(3)}  得到3位字符串
${rand_str(3, 10)}  得到3-10位字符串
```

```

以上yaml，生成的json数据示例
```
"json": {
    "password": "07d",
    "username": "c1c91161b4"
  }
```

## 7.5 fake 对象的使用

内置的 fake 对象 (注意是fake,不是faker, 因为faker 是模块名称，避免冲突) ，可以生成随机手机号，随机身份证，姓名等数据

```
获取当前时间:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      name: ${fake.name()}
      tel: ${fake.phone_number()}
      email: ${fake.email()}
  validate:
    - eq: [status_code, 200]

```

生成的测试数据
```
{'name': '王建平', 'tel': 13056609200, 'email': 'jluo@example.net'}
```

其它更多方法参考Faker模块提供的方法[https://www.cnblogs.com/yoyoketang/p/14869348.html](https://www.cnblogs.com/yoyoketang/p/14869348.html)


# 8 钩子功能

## 8.1 response 钩子功能
在发送请求的时候，我们希望在发送请求参数前，带上签名的值，或者返回的内容需要二次处理，解密后返回。
此功能我们可以用 hooks 钩子来实现
hooks 功能在v1.0.4版本上实现

requests 库只支持一个 response 的钩子，即在响应返回时可以捎带执行我们自定义的某些方法。
可以用于打印一些信息，做一些响应检查或想响应对象中添加额外的信息
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
import requests
url = 'https://httpbin.org/get'


def response_status(resopnse, *args, **kwargs):
    print('url', resopnse.url)
    resopnse.status = 'PASS' if resopnse.status_code < 400 else 'FAIL'


res = requests.get(url, hooks={'response': response_status})
print(res.status)
```
以上是基于requests 库的钩子功能实现的基本方式

## 8.2 yaml 用例中添加response 钩子

在yaml 文件中添加response 钩子功能，跟上面代码方式差不多, 有2种方式
- 1.写到config 全局配置，每个请求都会带上hooks
- 2.写到单个请求的request 下，仅单个请求会带上hooks功能

先看单个请求的response 钩子
test_hook1.yml
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/
config:
  name: post示例
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
    hooks:
      response: ['hook_response']
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
```

在 conftest.py 中注册钩子函数

```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/

def hook_response(response, *args, **kwargs):
    # print(response.text) 原始数据
    print("执行response hook 函数内容....")
    class NewResponse:
        text = '{"code": 0, "data": {"token": "yo yo"}}'  # response.text解密
        history = response.history
        headers = response.headers
        cookies = response.cookies
        status_code = response.status_code
        raw = response.raw
        is_redirect = response.is_redirect
        content = b'{"code": 0, "data": {"token": "yo yo"}}'  # response.text解密
        elapsed = response.elapsed

        @staticmethod
        def json():
            # 拿到原始的response.json() 后解码
            return {"code": 0, "data": {"token": "yo yo"}}

    return NewResponse

my_builtins.hook_response = hook_response
```

由于上面用例只在第一个请求中使用了hooks功能，所以第二个请求的断言`- eq: [$.code, 0]` 会失败

## 8.3 钩子方法调用语法
- 1.层级是在request 下
- 2.hooks 关键字对应的是一个字典 {"response": []}
- 3.response 的值可以是单个函数名称，也可以是多个`func1, func2`,或者是一个list类型[func1, func2]
- 4.response 的值必须是一个可以调用的函数，此函数需在conftest 中注册绑定到`my_builtins` 模块
- 5.调用的函数第一个参数是`response`， 可以重写response内容（如需要对返回结果解密），也可以不用重写

```
  request:
    method: POST
    url: http://httpbin.org/post
    hooks:
      response: ['hook_response']
```

## 8.4 config 全局钩子使用

在config 中配置全局hooks功能，格式如下
```
config:
  name: post示例
  hooks:
    response: ['hook_response']
```

test_hook2.yml完整示例
```
config:
  name: post示例
  hooks:
    response: ['hook_response']
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
    hooks:
      response: ['hook_response']
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
```

全局配置hooks， 那么该用例下所有的请求都会带上hooks

## 8.5 请求预处理钩子

如果需要对请求参数预处理，我们还新增了一个request 请求钩子，可以获取到发送请求时的request参数

在conftest.py 
```
# 作者-上海悠悠 微信/QQ交流:283340479
# blog地址 https://www.cnblogs.com/yoyoketang/


def func1(req):
    print(f'请求预处理：{req}')
    
    
def func2():
    print(f'请求预处理-----------')
    
    
my_builtins.func1 = func1
my_builtins.func2 = func2
```

在 yaml 文件中使用示例
```
config:
  name: post示例
teststeps:
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
    hooks:
      request: ['func1', 'func2']
      response: ['hook_response']
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
-
  name: post
  request:
    method: POST
    url: http://httpbin.org/post
    json:
      username: test
      password: "123456"
    hooks:
      response: ['hook_response']
  extract:
      url:  body.url
  validate:
    - eq: [status_code, 200]
    - eq: [headers.Server, gunicorn/19.9.0]
    - eq: [$.code, 0]
```

在config 中设置全局hooks示例
```
config:
  name: post示例
  hooks:
    request: ['func1', 'func2']
    response: ['hook_response']
```

由于request 变量是 pytest的一个内置fixture，此变量保留着，获取请求参数的函数使用`req` 代替。
利用request hook功能可以实现请求参数的预处理，比如请求 body 签名和加密处理等需求。

# 9 用例分层

当我们测试流程类的接口，需反复去调用同一个接口，就会想到复用API，在代码里面可以写成函数去调用。
那么在yaml 文件中，我们可以把单个API写到一个yaml 文件，测试用例去调用导入API。

我这里只分2层：API 层 和 Test case 用例层

- API 层: 描述接口request请求，可以带上validate 基本的校验
- Test case 用例层: 用例层多个步骤按顺序引用API

![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a3.png)

## 9.1 API 层示例

API 层只做接口的描述，一般放到项目根目录api目录下

api/login.yaml 示例
```
name: post
request:
    method: POST
    url: http://httpbin.org/post
    json:
        username: ${username}
        password: "123456"
validate:
    - eq: [status_code, 200]
```

如果有需要用到变量，比如登录用户名在不同用例中会用到不同的账号，那么可以使用变量 `${username}`
需注意的是，API 层不支持单独运行，因为它只是用例的一个部分，不能当成用例去执行，用例执行需使用 `test_*.yml` 命名

## 9.2 TestCase 层

用例层通过api 关键字导入需要的API，导入的路径是相对路径，需根据项目的根目录去导入。
比如我的项目结构是这样的
```
├─api
   └─ login.yml
├─testcase
   └─ test_login.yml
└─conftest.py
└─pytest.ini
```

那么不管用例文件`test_*.yml`在哪个目录，都是以项目根目录去导入API 的yaml文件
```
config:
    name: login case
    base_url: http://127.0.0.1:8000
    variables:
        username: "test123"
        password: "123456"


teststeps:
-
    name: step login1
    api: api/login.yml
    extract:
        url:  body.url
    validate:
        - eq: [status_code, 200]
        - eq: [ok, true]
-
    name: step login2
    api: api/login.yml
```

运行用例也是在项目根目录去执行 pytest 运行
```
pytest testcase
```


## 9.3 关于变量

API 层可以引用变量，引用变量的值都是从用例目录的variables 加载的变量，目前只支持config 设置用例全局变量
```
config:
    name: login case
    base_url: http://127.0.0.1:8000
    variables:
        username: "test123"
        password: "123456"
```

我们可以理解为API是用例的一个步骤，是用例的一部分，导入过去相当于复制request 请求到用例步骤里面。

## 9.4 关于校验

在API 层可以写一些基础的校验，比如校验状态码，我们一般不在API层写业务逻辑校验。
比如登录的用例，期望结果可以是登录成功，也可以是登录失败，那么业务逻辑的校验，应该在用例层去校验

```
-
    name: step login1
    api: api/login.yml
    extract:
        url:  body.url
    validate:
        - eq: [status_code, 200]
        - eq: [ok, true]
```

如果API 层和用例层都有validate 校验，最后会合并到一起校验。


# 10 写多个用例

一个yaml 文件中可以写多个用例，yaml 文件相当于py模块，每个用例相当于模块里面定义 pytest 的一个函数，
用例名称最好是test开头，如果不是test开头，也会帮你自动拼接成test开头的

## 10.1 实现原理

在 pytest 用例中，我们可以在一个模块写多个函数式的用例，每个用例test开头，如下
```
import pytest


def test1():
    """用例1"""
    print("hello 111")


def test2():
    """用例2"""
    print("hello 222")


def test3():
    """用例3"""
    print("hello 333")


if __name__ == '__main__':
    pytest.main(['-s', 'test_sample.py'])
```
执行后会看到3个用例
```
collected 3 items

test_sample.py hello 111
.hello 222
.hello 333
.

=============== 3 passed in 0.01s ===========
```

根据以上 pytest 的基本运行原理，于是我们也可以在yaml文件中写出同等的效果

```
    test1:
        name: 用例1
        print: hello 11111

    test2:
        name: 用例2
        print: hello 22222

    test3:
        name: 用例3
        print: hello 3333
```

输入 pytest 运行 yaml 用例文件
```

(venv) D:\demo>pytest test_case.yml -s
=================================== test session starts ===================================
platform win32 -- Python 3.8.5, pytest-7.2.0, pluggy-1.0.0
collected 3 items                                                                          

test_case.yml hello 11111
.hello 22222
.hello 3333
.

==================================== 3 passed in 0.15s ====================================
```

可以看出执行效果是完全一样的


## 10.2 重新定义了yaml用例格式

为了框架的可扩展性，config 和 teststeps 都不是必须的了，当然以前的格式还是会兼容

```
    config:
        name: demo

    teststeps:
    -
      name: GET请求示例
      request:
        method: GET
        url: http://httpbin.org/get
      validate:
        - eq: [status_code, 200]

    test1:
        name: 用例1
        print: hello 11111

    test2:
        name: 用例2
        print: hello 22222

```
用例部分支持2种格式，可以是一个键值对格式

```
    test1:
        name: 用例1
        print: hello 11111
```

也可以是一个list

```

    test1:
     -
        name: 用例1
        print: hello 11111
```

如果一个用例有多个步骤需要执行，那么用例应该是一个list，会按顺序去执行

```
    config:
        name: demo
    
    
    test1:
        name: 用例1
        print: hello 11111
    
    test2:
    -
        name: get
        request:
            method: GET
            url: http://httpbin.org/get
        validate:
          - eq: [status_code, 200]
    
    -
        name: post
        request:
            method: POST
            url: http://httpbin.org/post
            json:
              username: test
              password: "123456"
        validate:
          - eq: [status_code, 200]
```

## 10.3 支持中文命名

用例的函数名称也可以使用中文命名了，这样更直观

```
config:
    name: demo


用例演示1:
    name: 用例1
    print: hello 11111

用例是多个步骤2:
-
    name: get
    request:
        method: GET
        url: http://httpbin.org/get
    validate:
      - eq: [status_code, 200]

-
    name: post
    request:
        method: POST
        url: http://httpbin.org/post
        json:
          username: test
          password: "123456"
    validate:
      - eq: [status_code, 200]
```

原有的用例规则不变，只是`teststeps` 不是必须的关键字，可以用其它的名称，也可以继续使用`teststeps` （为了兼容大家的使用习惯） 

# 11 日志功能

pytest 的日志分2个部分：
- console 控制台输出的日志
- log_file  保存到本地文件的日志

本插件默认情况下会记录运行日志保存在项目根目录logs下，以当前时间保存txt文本日志内容。
日志默认保存info级别。
console 控制台默认不输出日志

## 11.1 开启 console 控制台日志

控制台直接运行 pytest 是不会用日志输出的，因为默认仅输出 warning 以上的级别日志
有3种方式启动console日志

方法1：命令行带上`--log-cli-level`参数，设置日志级别
```
>pytest --log-cli-level=info
```
方法2： pytest.ini 配置开启日志，并且设置日志级别
```
[pytest]

log_cli = true
log_cli_level = info
```
方法3： pytest -o方式重写（即覆盖ini文件中的log相关的命令行参数）
```
pytest -o log_cli=true -o log_cli_level=INFO
```

即可在控制台看到日志
```
-------------------------------------------- live log call --------------------------------------------
2022-12-08 08:30:34 [INFO]: 执行文件-> test_demo.yml
2022-12-08 08:30:34 [INFO]: base_url-> None
2022-12-08 08:30:34 [INFO]: variables-> {}
2022-12-08 08:30:34 [INFO]: 运行 teststeps
2022-12-08 08:30:34 [INFO]: --------  request info ----------
POST http://httpbin.org/post
{
  "method": "POST",
  "url": "http://httpbin.org/post",
  "json": {
    "username": "test",
    "password": "123456"
  }
}
2022-12-08 08:30:35 [INFO]: ------  response info  200 OK  0.495961s------
```

## 11.2 自定义 console 控制台日志

日志的格式和时间格式也可以自定义设置

```
[pytest]

log_cli = true
log_cli_level = info
log_cli_format = %(asctime)s %(filename)s:%(lineno)s [%(levelname)s]: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

## 11.3 自定义保存日志文件

本插件默认情况下会记录运行日志保存在项目根目录logs下，以当前时间保存txt文本日志内容。
日志默认保存info级别。
如果你想改变这些默认的行为，自定义日志文件目录和名称，可以在pytest.ini 配置日志文件
(log_file 相关的结果是保存日志文件到本地)
```
[pytest]

log_cli = true
log_cli_level = info
log_cli_format = %(asctime)s %(filename)s:%(lineno)s [%(levelname)s]: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

log_file = ./yoyo.log
log_file_level = debug
log_file_format = %(asctime)s %(filename)s:%(lineno)s [%(levelname)s]: %(message)s
log_file_date_format = %Y-%m-%d %H:%M:%S
```

## 11.4 命令行参数配置

log日志的配置也可以用命令行参数配置(pytest -h可以查看)
```
 --no-print-logs       　　　　　　 disable printing caught logs on failed tests.
 --log-level=LOG_LEVEL     　　　　logging level used by the logging module
 --log-format=LOG_FORMAT　　　　　　log format as used by the logging module.
 --log-date-format=LOG_DATE_FORMAT　　　　　　log date format as used by the logging module.
 --log-cli-level=LOG_CLI_LEVEL　　　　　　　　cli logging level.
 --log-cli-format=LOG_CLI_FORMAT　　　　　　　　log format as used by the logging module.
 --log-cli-date-format=LOG_CLI_DATE_FORMAT　　　　　　log date format as used by the logging module.
 --log-file=LOG_FILE   　　　　　　　　　　　　path to a file when logging will be written to.
 --log-file-level=LOG_FILE_LEVEL　　　　　　log file logging level.
 --log-file-format=LOG_FILE_FORMAT　　　　　　log format as used by the logging module.
 --log-file-date-format=LOG_FILE_DATE_FORMAT　　　　　　log date format as used by the logging module.
```

还可以使用 `pytest -o` 方式重写（即覆盖 ini 文件中的 log 相关的命令行参数）

```
pytest pytest  test_log.py -o log_cli=true -o log_cli_level=INFO
```

# 12 allure 报告

本插件是基于 pytest 框架开发的，所以 pytest 的插件都能使用
allure 报告功能在 v1.0.8 版本上实现

## 12.1 allure 环境准备

allure 是一个命令行工具，需要去github上下载最新版[https://github.com/allure-framework/allure2/releases](https://github.com/allure-framework/allure2/releases)

allure  命令行工具是需要依赖jdk 环境，环境内容自己去搭建了

## 12.2 生成 allure 报告

在用例所在的目录执行命令, `--alluredir` 是指定报告生成的目录

```
pytest --alluredir ./report
```

打开allure 报告执行命令
```
>allure serve ./report
```

## 12.3 查看报告

首页显示

![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a4.png)
图表查看

![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a5.png)
用例详情根据yaml文件名称和用例名称展示内容

![](https://gitee.com/yoyoketang/pytest-yaml-yoyo/raw/master/tests/images/a6.png)


# 13 全局 base_url

一个完整的url 地址由环境地址和接口地址拼接而成，环境地址是可变的，可以部署到测试环境，uat联调环境等不同的环境。
不管部署到哪个环境，接口的地址是不可变的，通常需要一个全局base_url 地址做到环境可切换。
pip 安装插件

```
pip install pytest-yaml-yoyo
```

 base_url 全局配置功能在 v1.0.9 版本上实现

## 13.1 环境地址

在接口测试中，通常会把环境 base_url 地址独立出来
比如一个完整的请求`http://httpbin.org/get` 那么可以分成环境地址`http://httpbin.org` 和 接口地址 `/get`

在 yaml 用例中，可以把 base_url 单独拿出来放到 config 下

```
config:
  base_url: http://httpbin.org

get示例:
  name: get demo
  request:
    method: GET
    url: /get
  validate:
    - eq: [status_code, 200]

post示例:
  name: get demo
  request:
    method: POST
    url: /post
  validate:
    - eq: [status_code, 200]
```

## 13.2 全局 base_url 配置

从项目的角度讲，测试项目接口的 base_url 都是一样的，所以我们只需全局设置一个就行了，不需要每个yaml 文件中重复去写。
于是可以在pytest.ini 里面配置全局base_url

```
[pytest]

base_url = http://httpbin.org
```

那么yaml用例就不需要写 base_url 了，默认会引用pytest.ini的全局配置

yaml 用例1
```
config:
  name: demo1

get示例:
  name: get demo
  request:
    method: GET
    url: /get
  validate:
    - eq: [status_code, 200]
```

yaml 用例2
```
config:
  name: demo2

post示例:
  name: get demo
  request:
    method: POST
    url: /post
  validate:
    - eq: [status_code, 200]
```

除了可以在pytest.ini 配置base_url 参数，也可以通过命令行参数` --base-url `去设置 
```
pytest --base-url=http://httpbin.org
```

## 13.3 复杂情况

当设置了全局base_url 后，有部分用例的环境地址不是同一个的时候，我们可以在yaml文件中config 配置 base_url 去覆盖全局配置环境地址。

```
config:
  base_url: http://httpbin.org

get示例:
  name: get demo
  request:
    method: GET
    url: /get
  validate:
    - eq: [status_code, 200]

```

或者请求 url 地址用绝对地址
```
config:
  name: demo

get示例:
  name: get demo
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
```

## 13.4 使用优先级

环境地址优先级使用如下：
1.全局配置命令行参数` --base-url `优先级大于 pytest.ini 文件中的 base_url 配置。
2.yaml 文件 config 中的base_url 优先级大于全局配置
3.request 请求的url 如果是绝对地址，那么base_url 无效

总的来说 : url 绝对地址 > config 中的base_url >  pytest.ini 文件中的base_url > 命令行参数` --base-url `

# 14 全局项目配置

当我们在测试环境写好自动化的代码，领导说你把代码部署到联调环境再测一测，这时候去改用例里面的配置是很痛苦的。
所以我们在设计自动化用例的时候，就先要想到多环境的配置与切换。

## 14.1 多环境配置

如果需用到多套环境 test/uat 等，那么应该在用例的根目录(pytest.ini 同级文件)创建一个config.py 文件
pip 安装插件
```
pip install pytest-yaml-yoyo
```
多套环境切换功能在 v1.0.10 版本上实现

```

class Config:
    """多套环境的公共配置"""
    version = "v1.0"


class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://192.168.1.1:8000'
    MYSQL_HOST = "192.168.1.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "xxx"   # 连接数据的库名


class UatConfig(Config):
    """联调环境"""
    BASE_URL = 'http://192.168.1.3:8080'
    MYSQL_HOST = "http://192.168.1.3"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "654321"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "xxx"  # 连接数据的库名


# 环境关系映射，方便切换多环境配置
env = {
    "test": TestConfig,
    "uat": UatConfig
}
```

按以上的配置格式，配置不同的环境，最后做一个环境名称和配置的映射关系，必须是 env 命名，格式如下
```
env = {
    "test": TestConfig,
    "uat": UatConfig
}
```

那么在执行用例的时候，可以选择执行test 环境还是uat 环境，有 2 种方式可以配置待执行的环境

方法一: 在pytest.ini 中配置
```
[pytest]


env = test
```

方法二: 执行 pytest 命令的时候设置
```
pytest --env test
```

如果2个地方都有设置，那么优先级是：命令行参数` --env test` 大于 pytest.ini 中配置`env = test`.


## 14.2 测试环境的 BASE_URL

在上一篇中讲到 [pytest + yaml 框架 -11.全局 base_url 配置](https://www.cnblogs.com/yoyoketang/p/16970491.html)
```
环境地址优先级使用如下：
1.全局配置命令行参数--base-url优先级大于 pytest.ini 文件中的base_url 配置。
2.yaml 文件 config 中的base_url 优先级大于全局配置
3.request 请求的url 如果是绝对地址，那么base_url 无效
总的来说 : url 绝对地址 > config 中的base_url > 命令行参数--base-url > pytest.ini 文件中的base_url
```
这里我们新增了一个在config.py 中也可以配置全局的base_url （config.py 中的配置用大写命名 BASE_URL）


如果在 config.py 中配置全局的 BASE_URL ，那么也会生效。优先级会低于命令行和 pytest.ini 的配置

总的来说：url 绝对地址 > config 中的base_url > 命令行参数--base-url > pytest.ini 文件中的 base_url > config.py 的 BASE_URL

## 14.3 多个base_url 切换

有同学提到说，如果一个用例中有多个base_url 需要切换，该如何解决？

我们在配置项中BASE_URL 项是设置默认的全局base_url地址，如果有多个地址，我们还可以用其它的配置参数，比如 `BLOG_URL` 和 `DEMO_URL`
```

class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://192.168.1.1:8000'
    BLOG_URL = 'https://www.cnblogs.com'
    DEMO_URL = 'http://httpbin.org'
    MYSQL_HOST = "192.168.1.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "xxx"   # 连接数据的库名
```

上面的配置中，我们就配置了3个环境地址
```
    BASE_URL = 'http://192.168.1.1:8000'
    BLOG_URL = 'https://www.cnblogs.com'
    DEMO_URL = 'http://httpbin.org'
```

在yaml 用例中，如果没有传base_url, 那么会用默认的 `BASE_URL = 'http://192.168.1.1:8000'`

使用示例

```
config:
  name: 示例

用例:
-
  name: GET
  request:
    method: GET
    url: /get
  validate:
    - eq: [status_code, 200]
```

当一个接口中同时用到3个测试地址 `BASE_URL`、`BLOG_URL`、`DEMO_URL` 时，可以通过 env 变量取值，如: `${env.BLOG_URL}`

```
config:
  name: 示例

用例:

-
  name: GET
  request:
    method: GET
    url: ${env.BLOG_URL}/yoyoketang
  validate:
    - eq: [status_code, 200]

-
  name: GET
  request:
    method: GET
    url: ${env.DEMO_URL}/get
  validate:
    - eq: [status_code, 200]

-
  name: GET
  request:
    method: GET
    url: /get
  validate:
    - eq: [status_code, 200]
```

## 14.4 其它配置参数

如果配置中需要加其它配置参数
```
class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://192.168.1.1:8000'
    USER = 'test'
    TEL = '100860000'

```

那么在用例中引用配置参数可以用 `${env.配置参数}` 取到配置中的值。


# 15 mysql 数据库配置

如果用例中需要执行mysql 数据库，或者在断言的时候需要查询mysql 数据库。先在config.py 中完成配置

```
class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://192.168.1.1:8000'
    MYSQL_HOST = "192.168.1.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_PORT = 3306
    MYSQL_DATABASE = "xxx"   # 连接数据的库名
```

当完成了MYSQL 相关的五个配置，那么有个内置的函数可以使用
- query_sql(sql）   查询sql, 查询无结果返回None, 查询只有一个结果返回dict, 查询多个结果返回list of dict
- execute_sql(sql)  执行sql, 操作新增，修改，删除的sql


## 15.1 断言执行sql

使用示例

```
config:
  base_url: http://192.168.1.1:8000
  variables:
    username: test
    sql: select * from auth_user where username like 'test';

登录:
    name: step login
    request:
        url: /api/v1/login
        method: POST
        json:
            username: ${username}
            password: "123456"
    extract:
        token: $.token
    validate:
        - eq: [status_code, 200]
        - eq: [ok, true]
        - eq: [$.username, '${query_sql(sql).username}']
```

以上示例是断言的时候，执行sql，获取数据库的值
```
- eq: [$.username, '${query_sql(sql).username}']
```

可以开启日志
```
[pytest]

log_cli = true
log_cli_level = debug
env = test

```
查看运行日志
```
body:
     {"code": 0, "msg": "login success!", "username": "test", "token": "6112772900193da079e9fcc857613f6125
3648fd"}

2022-12-13 10:34:54 [INFO]: extract 提取变量-> {'token': '6112772900193da079e9fcc857613f61253648fd'}
2022-12-13 10:34:54 [DEBUG]: query sql: select * from auth_user where username like 'test';!
2022-12-13 10:34:54 [INFO]: query result: {'id': 2, 'password': 'pbkdf2_sha256$100000$rSQNBkIc2xOm$VGXiUZk
dsIueT/AsoPwlFSEL1vGODsK7eIjK0nawH/M=', 'last_login': None, 'is_superuser': 0, 'username': 'test', 'first_
name': '', 'last_name': '', 'email': '478391@qq.com', 'is_staff': 0, 'is_active': 1, 'date_joined': dateti
me.datetime(2022, 11, 11, 21, 22, 59, 971425)}
2022-12-13 10:34:54 [INFO]: validate 校验内容-> [{'eq': ['status_code', 200]}, {'eq': ['ok', True]}, {'eq'
: ['$.username', 'test']}]
2022-12-13 10:34:54 [INFO]: validate 校验结果-> eq: [200, 200]
2022-12-13 10:34:54 [INFO]: validate 校验结果-> eq: [True, True]
2022-12-13 10:34:54 [INFO]: validate 校验结果-> eq: [test, test]

```

从返回的body 里面提取username 使用表达式`$.username`, 得到实际结果"test"
 '${query_sql(sql).username}' 表达式会先调用query_sql(sql) 函数，引用前面设置的变量sql, 得到结果
```
{'id': 2, 'password': 'pbkdf2_sha256$100000$rSQNBkIc2xOm$VGXiUZk
dsIueT/AsoPwlFSEL1vGODsK7eIjK0nawH/M=', 'last_login': None, 'is_superuser': 0, 'username': 'test', 'first_
name': '', 'last_name': '', 'email': '478391@qq.com', 'is_staff': 0, 'is_active': 1, 'date_joined': dateti
me.datetime(2022, 11, 11, 21, 22, 59, 971425)}
```
得到的结果是一个字典，字典对象可以继续取值，于是`'${query_sql(sql).username}'` 就可以得到期望结果 "test"


## 15.2 用例的参数也可以查询sql

如果用例的参数，需要从sql中取值，我们也可以先定义变量，在用例中引用query_sql(sql) 函数

```
config:
  variables:
    sql: select * from auth_user where username like 'test';

登录:
    name: step login
    request:
        url: /api/v1/login
        method: POST
        json:
            username: ${query_sql(sql).username}
            password: "123456"
    extract:
        token: $.token
        x: ${query_sql(sql).username}
    validate:
        - eq: [status_code, 200]
        - eq: [ok, true]
        - eq: [$.username, test]
```
 
extract 中也可以支持执行sql，得到提取结果

```
  extract:
        token: $.token
        x: ${query_sql(sql).username}
```

## 15.3 用例前置和后置执行sql

如果需要在用例的前置和后置中执行sql， 可以用到hook 机制，在请求前和请求后执行函数
参考前面这篇[pytest + yaml 框架 -6.hooks 钩子功能实现](https://www.cnblogs.com/yoyoketang/p/16938512.html)

# 16 钉钉机器人通知

当用例执行完成后，希望能给报告反馈，常见的报告反馈有：邮箱/钉钉群/飞书/企业微信 等。
pip 安装插件
```
pip install pytest-yaml-yoyo
```
钉钉机器人通知测试结果功能在v1.1.1版本实现

## 16.1 钉钉机器人设置

钉钉机器人的设置请参考官方API文档[https://open.dingtalk.com/document/group/custom-robot-access](https://open.dingtalk.com/document/group/custom-robot-access)

我们主要得到Webhook地址上面的access_token 值
![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221213232504844-820155263.png)

自定义关键字，默认：测试报告，也可以自定义

![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221213232557051-1430273687.png)

加签 的值，可以不勾选，也可以勾选。

总的来说，需要记住3个地方：
- access_token 复制Webhook地址上面的access_token 值
- 自定义关键字  默认：测试报告，也可以自定义其他名称，如果这里改了，后面的配置的title值也要改成一样
-  加签 的值，可以不勾选，也可以勾选。如果勾选了，后面需配置secret 值

## 16.2 config 中配置 DING_TALK 项

在config 中配置 DING_TALK, 只有 access_token 值是必须项， 如果配置了 DING_TALK ，那么就会自动启动发送钉钉机器人通知。
如果不启动钉钉机器人通知测试报告，那么把此项注掉即可。
 
```
class Config:
    version = "v1.0"


class TestConfig(Config):
    """测试环境"""
    BASE_URL = 'http://127.0.0.1:8000'
    # 钉钉群机器人通知
    DING_TALK = {
        "access_token": "d2433d2b16cc85*************************************",
    }


class UatConfig(Config):
    """联调环境"""
    BASE_URL = 'http://192.168.1.1:8001'



# 环境关系映射，方便切换多环境配置
env = {
    "test": TestConfig,
    "uat": UatConfig
}

```

在pytest.ini 中配置
```
[pytest]


env = test
```

DING_TALK 相关参数说明
- access_token: 钉钉群自定义机器人access_token
- secret: 机器人安全设置页面勾选"加签"时需要传入的密钥
- param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
- param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理
- param title: 首屏会话透出的展示内容
- param text: markdown格式的消息内容
- param is_at_all: @所有人：True，否则为：False（可选）, 默认False
- param at_mobiles: 被@人的手机号, 手机号可以是一个或者多个，写到list
- param at_dingtalk_ids: 被@用户的UserId（企业内部机器人可用，可选），可以是一个或者多个，写到list
- param is_auto_at: 是否自动在text内容末尾添加@手机号，默认自动添加，也可设置为False，然后自行在text内容中自定义@手机号的位置，才有@效果，支持同时@多个手机号（可选）


运行用例后会自动在钉钉群发送通知

![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221214075917320-900139319.png)


## 16.3 加签值配置

如果这里没有勾选 加签 值
![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221213232557051-1430273687.png)
那么只需要配置一个 access_token 即可

```
DING_TALK = {
        "access_token": "d2433d2b16cc85943*********************************",
    }
```

如果这里勾选 加签 值， 那么需同时配置 access_token 和 secret 值
```
DING_TALK = {
        "access_token": "d2433d2b16cc85943*********************************",
        "secret": "**************************"
    }
```



## 16.3 设置@指定的人

奈特指定的人有3个配置可以选择
- is_at_all  @所有人：True，否则为：False（可选）
- at_mobiles: 被@人的手机号，可以是一个或者多个，写到list
- at_dingtalk_ids: 被@用户的UserId（企业内部机器人可用，可选），可以是一个或者多个，写到list

使用示例
```
 DING_TALK = {
        "access_token": "d2433d2b16cc85****************",
        "at_mobiles": ["15000xxxxxxx", "15001xxxxxxx"]
    }
```

于是就可以看到上图的效果，在内容后面带上`@张三`的样式

## 16.4 设置 title 和 内容

title 的名称必须与自定义关键字名称保持一致
![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221213234034035-889157404.png)

```
 DING_TALK = {
        "access_token": "d2433d2b16******************",
        "title": "测试报告",
        "at_mobiles": ["15000xxxxxxx", "15001xxxxxxx"]
    }
```

报告的 text 内容， 也就是我们看到的

```
执行结果:

- 运行环境: test
- 运行base_url: http://127.0.0.1:8000
- 持续时间:  0.37 秒

本次运行结果:

- 总用例数: 3
- 通过用例：3
- 失败用例： 0
- 异常用例： 0
- 通过率： 100.0 %
```

text 的内容，默认是上面的这些，支持markdown 文档格式，如果你需要添加额外的内容，比如加上allure报告地址，那么可以用 text 字段追加内容

```
 DING_TALK = {
        "access_token": "d2433d2b16cc8594348**************",
        "title": "测试报告",
        "at_mobiles": ["15000xxxxxxx", "15001xxxxxxx"],
        "text": ""text": "- 查看报告：[allure报告地址](https://www.cnblogs.com/yoyoketang/)""
    }
```

把上面的`https://www.cnblogs.com/yoyoketang/` 换成你自己的allure报告地址即可

于是看到以下的效果

![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221214075952180-2027249947.png)


总的来说，整个配置都是傻瓜式的，配置非常简单。

# 17 文件上传

本插件集成了 requests_toolbelt 插件处理`Content-Type: multipart/form-data` 类型文件上传接口。

## 17.1 文件上传multipart/form-data 

用fiddler抓包，查看抓到的接口，以下这种接口就是multipart/form-data

- Content-Type: multipart/form-data
- body参数是这种格式：

-----------------------------22165374713946
Content-Disposition: form-data; title="localUrl"

yoyoketang.png
-----------------------------22165374713946
Content-Disposition: form-data; name="imgFile"; filename="yoyoketang.png"
Content-Type: image/png

![](http://images2017.cnblogs.com/blog/1070438/201712/1070438-20171205232930613-2074674964.png)

## 17.2 在yaml 文件中示例

在postman 中，可以直接选择一个文件上传，非常方便

![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221217162337002-1574943477.png)

我们在yaml中也一样，支持文件类的参数，需单独拿出来放到 files 字段里面。

test_upfile.yml 示例
```
文件上传:
  name: upload file
  request:
      url: http://127.0.0.1:8000/api/v1/upfile/
      method: POST
      data:
          title: 文件上传
      files:
          file: data/abc.jpg
```

文件abc.jpg 需放到项目根目录data下

![](https://img2023.cnblogs.com/blog/1070438/202212/1070438-20221217162549076-1639541804.png)

files 里面需要传的具体字段，需根据接口文档定义的参数名称。

当然你把其它字符串字段一起放到files 里面也没问题

```
文件上传:
  name: upload file
  request:
      url: http://127.0.0.1:8000/api/v1/upfile/
      method: POST
      files:
          title: 文件上传
          file: data/abc.jpg
```
（本插件也是根据你是否在 request 中传了 files 字段来判断是不是需要上传文件）

# 18 sleep和skip、skipif 功能

v1.1.3 发布新增3个关键字
- 1.sleep  添加用例之间的sleep 等待时间
- 2.skip   跳过用例功能
- 3.skipif   条件为真时跳过用例

使用示例
```yaml
config:
  variables:
    x: 1
get请求:
  name: GET请求示例
  sleep: ${x}
  skip: 原因-功能未实现
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
get1请求:
-
  name: GET请求示例
  sleep: ${x}
  skipif: 2>1
  request:
    method: GET
    url: http://httpbin.org/get
  validate:
    - eq: [status_code, 200]
```


目前大部分功能和需求已经实现，完全可以在项目中投入和使用了，如果有bug请及时通知，会立马修复。
后续计划：
- 1.yaml 数据格式校验
- 2.其它细节优化

更多功能持续开发中....大家有好的建议想法也欢迎提出, 微信交流联系wx:283340479

# 19 联系我们

作者-上海悠悠 微信/QQ交流:283340479
blog地址 https://www.cnblogs.com/yoyoketang/
