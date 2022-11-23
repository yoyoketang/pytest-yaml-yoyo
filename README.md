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

# 其它功能

目前第一个版本只实现了一些基础功能，还有接口的提取extract功能还未实现。
后续计划：
1、完善extract功能
2、实现多个接口步骤的参数关联
3、结合 allure 生成报告
4、赋值函数功能使用
5、yaml 中调用 fixture 功能实现
6、全局使用一个token，仅登录一次，完成全部用例测试
7、对yaml数据格式校验
8、添加日志
9、新增另外一套yaml用例规范

更多功能持续开发中....大家有好的建议想法也欢迎提出， 微信交流联系wx:283340479
