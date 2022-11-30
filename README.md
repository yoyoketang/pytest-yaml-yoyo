# 说明

基于 httprunner 框架的用例结构，我自己开发了一个pytest + yaml 的框架，那么是不是重复造轮子呢？
不可否认 httprunner 框架设计非常优秀，但是也有缺点，httprunner3.x的版本虽然也是基于pytest框架设计，结合yaml执行用例，但是会生成一个py文件去执行。
在辅助函数的引用也很局限，只能获取函数的返回值，不能在yaml中对返回值重新二次取值。
那么我的这个框架，就是为了解决这些痛点。。。。

# 环境准备

Python 3.8版本
Pytest 7.2.0 最新版

pip 安装插件

```
pip install pytest-yaml-yoyo
```


# 第一个 hello world

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
- config  是必须的里面必须有 name 用例名称，base_url 和 variables 是可选的
- teststeps 用例的步骤，用例步骤是一个array 数组类型，可以有多个步骤

从上面的运行可以看出，request 不是必须的，我们可以直接调用python内置函数print 去打印一些内容了。

# 一个简单的 http 请求

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

# 再来一个post请求

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

# validate校验

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

# 变量的声明与引用

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

![](https://img2022.cnblogs.com/blog/1070438/202211/1070438-20221123143938244-1854561508.png)

# extract 提取接口返回参数关联
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

# 参数关联

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

# extract 提取结果二次取值

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

# parameters 参数化的实现

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

## 使用 fixtures 功能实现参数化

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


## parameters 实现参数化

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


# yaml 中调用内置方法

pytest-yaml-yoyo 插件使用了强大的jinja2 模板引擎，所以我们在yaml文件中可以写很多python内置的语法了。
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

# 字典对象取值

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

# 自定义函数功能

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

# 函数传参数

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

# 函数返回的结果也能二次取值

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


# response 钩子功能
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

# yaml 用例中添加response 钩子

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

在conftest.py 中注册钩子函数

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

钩子方法调用语法
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

# config 全局使用

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

# 请求预处理钩子

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

# 其它功能

目前第一个版本只实现了一些基础功能，还有一些功能待实现。
后续计划：
- 1、结合 allure 生成报告
- 2、对 yaml 数据格式校验
- 3、添加日志
- 4、新增另外一套yaml用例规范

更多功能持续开发中....大家有好的建议想法也欢迎提出， 微信交流联系wx:283340479

# 版本变更记录

v1.0.0
发布的第一个版本（已删除)

v1.0.1  发布时间 2022.11.23
可以安装的第一个版本

- 1.实现基础的 pytest 命令 执行yaml 文件用例功能

v1.0.2 发布时间 2022.11.24

- 1.新增extract 关键字，在接口中提取返回结果
- 2.参数关联，上一个接口的返回值可以作为下个接口的入参

详细功能参阅 extract 关键字文档

v1.0.3 发布时间 2022.11.28

- 1.config 新增 fixtures 关键字，在yaml 用例中传fixture功能和参数化功能
- 2.config 新增 parameters，用例参数化实现

详细功能参阅 parameters参数化 关键字文档

v1.0.4 发布时间 2022.11.30
hooks 钩子功能实现

- 1.request 钩子对请求参数预处理
- 2.response 钩子对返回结果处理

详细功能参阅 hooks 钩子 关键字文档