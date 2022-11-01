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

get_table = on_command("课表")
current_path = path.abspath(__file__)
current_dir = path.dirname(current_path)
config = rtoml.load(open(current_dir + "/config.toml", "r"))
scheme = Parse(config)
group_id = scheme.settings["group_id"]
moments = ring_bell()
require("nonebot_plugin_apscheduler")


@get_table.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if not plain_text:
        args = get_week_order()
    if gen_week_img(int(str(args))):
        img_path = "file:///" + str(current_dir) + f"/tmp/{args}_week.jpg"
        msg = Message([
            MessageSegment(type="text", data={"text": f"你要的第{args}课表，请过目："}),
            MessageSegment(type="image", data={"file": img_path})
        ])
        await bot.send(event=event, message=msg)


@scheduler.scheduled_job('cron', hour=8, minute=0)
async def _():
    bot = get_bot()
    if good_morning():
        await bot.send_group_msg(group_id=group_id, message="糟糕，有早八")
    else:
        await bot.send_group_msg(group_id=group_id, message="无早八")


for i in range(0, 6):
    hour = moments[i][0]
    minute = moments[i][1]


    @scheduler.scheduled_job('cron', hour=hour, minute=minute)
    async def _():
        bot = get_bot()
        await bot.send_group_msg(group_id=group_id, message=course_reflection())
