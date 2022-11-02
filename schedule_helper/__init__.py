from os import path

import rtoml
from nonebot import Bot, require, get_bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command
from nonebot_plugin_apscheduler import scheduler

from .gen_img import gen_week_img
from .hourgalss import get_week_order, good_morning, ring_bell, course_reflection
from .parse_config import Parse

# “课表”命令 时间响应器
get_table = on_command("课表")
# 获取绝对路经
current_path = path.abspath(__file__)
current_dir = path.dirname(current_path)
# 导入并解析配置
config = rtoml.load(open(current_dir + "/config.toml", "r"))
scheme = Parse(config)
# 从配置中获取需要管理的 QQ 群
group_id = scheme.settings["group_id"]
# 获取需要上课提示的时间点
moments = ring_bell()
# 注入定时提醒插件
require("nonebot_plugin_apscheduler")


@get_table.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    """获取课表命令响应逻辑

    Args:
        bot (Bot): 当前机器人
        event (GroupMessageEvent): 群消息事件
        args (Message, optional): 消息命令参数. Defaults to CommandArg().
    """
    # 从命令参数中提取纯文本
    plain_text = args.extract_plain_text()
    # 若不存在参数，根据当前周次自动赋值参数
    if not plain_text:
        args = get_week_order()
    # 生成图片后，发送图片
    if gen_week_img(int(str(args))):
        # 图片路径
        img_path = "file:///" + str(current_dir) + f"/tmp/{args}_week.jpg"
        # 需要发送的消息
        msg = Message([
            MessageSegment(type="text", data={"text": f"你要的第{args}课表，请过目："}),
            MessageSegment(type="image", data={"file": img_path})
        ])
        # 调用发送函数
        await bot.send(event=event, message=msg)


@scheduler.scheduled_job('cron', hour=8, minute=0)
async def _():
    # 获取当前机器人
    bot = get_bot()
    # 根据早八函数返回值决定发送消息的内容
    if good_morning():
        await bot.send_group_msg(group_id=group_id, message="糟糕，有早八")
    else:
        await bot.send_group_msg(group_id=group_id, message="无早八")


#  注册课程提示器，每天需要注册六个
for i in range(0, 6):
    hour = moments[i][0]
    minute = moments[i][1]


    @scheduler.scheduled_job('cron', hour=hour, minute=minute)
    async def _():
        bot = get_bot()
        await bot.send_group_msg(group_id=group_id, message=Message(course_reflection()))
