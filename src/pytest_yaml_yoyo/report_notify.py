from dingtalkchatbot.chatbot import DingtalkChatbot

"""
机器人初始化
    :param access_token: 钉钉群自定义机器人access_token
    :param secret: 机器人安全设置页面勾选"加签"时需要传入的密钥
    :param pc_slide: 消息链接打开方式，默认False为浏览器打开，设置为True时为PC端侧边栏打开
    :param fail_notice: 消息发送失败提醒，默认为False不提醒，开发者可以根据返回的消息发送结果自行判断和处理

钉钉机器人通知报告
markdown类型
        :param title: 首屏会话透出的展示内容
        :param text: markdown格式的消息内容
        :param is_at_all: @所有人时：true，否则为：false（可选）
        :param at_mobiles: 被@人的手机号
        :param at_dingtalk_ids: 被@用户的UserId（企业内部机器人可用，可选）
        :param is_auto_at: 是否自动在text内容末尾添加@手机号，默认自动添加，也可设置为False，然后自行在text内容中自定义@手机号的位置，才有@效果，支持同时@多个手机号（可选）
        :return: 返回消息发送结果
"""


def ding_ding_notify(
        access_token, secret=None, pc_slide=False, fail_notice=False,
        title="测试报告", text="## 测试报告", is_at_all=False,
        at_mobiles=None, at_dingtalk_ids=None, is_auto_at=True, *args, **kwargs):  # noqa
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={access_token}'
    ding = DingtalkChatbot(webhook=webhook, secret=secret, pc_slide=pc_slide, fail_notice=fail_notice)
    ding.send_markdown(
        title=title, text=text, is_at_all=is_at_all,
        at_mobiles=at_mobiles if at_mobiles else [],
        at_dingtalk_ids=at_dingtalk_ids if at_dingtalk_ids else [],
        is_auto_at=is_auto_at
    )
