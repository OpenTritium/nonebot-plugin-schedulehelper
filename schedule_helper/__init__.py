from os import path

from nonebot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin.on import on_command

from .gen_img import gen_week_img
from .hourgalss import get_week_order

get_table = on_command("课表")

current_path = path.abspath(__file__)
current_dir = path.dirname(current_path)


@get_table.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    img_path = "file:///" + str(current_dir) + f"/tmp/{args}_week.jpg"
    msg = Message([
        MessageSegment(type="text", data={"text": f"你要的第{args}课表，请过目："}),
        MessageSegment(type="image", data={"file": img_path})
    ])
    plain_text = args.extract_plain_text()
    if not plain_text:
        args = get_week_order() + 1
    if gen_week_img(int(str(args))):
        await bot.send(event=event, message=msg)
