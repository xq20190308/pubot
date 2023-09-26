from nonebot import get_driver, require
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_datastore import get_plugin_data, get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

import littlebot.plugins.pu.dataModel as dataModel
import littlebot.plugins.pu.generateData as generateData
import littlebot.plugins.pu.pu
from .config import Config

require("nonebot_plugin_apscheduler")
import littlebot.plugins.pu.dataModel

require("nonebot_plugin_datastore")
plugin_data = get_plugin_data()
__plugin_meta = PluginMetadata(
    name="PU",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

get_event_list_command = on_command("获取活动列表", rule=to_me(), priority=10, block=True)
get_filtered_event_list_command = on_command("过滤活动列表", rule=to_me(), priority=10, block=True)
join_event_command = on_command("活动报名",rule=to_me(),priority=10,block=True)


@get_event_list_command.handle()
async def get_event_list_function(bot: Bot, session: AsyncSession = Depends(get_session), args: Message = CommandArg()):
    force_flush_flag = False

    if args.extract_plain_text():
        if "force_flush" in args.extract_plain_text():
            force_flush_flag = True
    event_list = generateData.check_type(await pu.getEventList(4, session, force_flush_flag))
    await bot.send_private_msg(user_id=3453642726, message=event_list)
    await session.commit()


@get_filtered_event_list_command.handle()
async def handel(args: Message = CommandArg(), matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="search_field",message=args)


@get_filtered_event_list_command.got("search_field", prompt="请输入过滤字段")
async def handel(search_field: str = ArgPlainText(),matcher=Matcher):
    search_field = search_field.strip()
    matcher.set_arg("search_field",search_field.strip())
    if search_field not in ["id", "title", "category", "isJoin"]:
        await get_filtered_event_list_command.reject(f"你输入的{search_field}暂不支持检索，请重新输入")


@get_filtered_event_list_command.got("search_value", prompt="请输入过滤值")
async def handel2(bot:Bot,search_value: str = ArgPlainText(),matcher=Matcher,session:AsyncSession = Depends(get_session)):
    event_list = generateData.check_type(await pu.get_filtered_event_list(matcher.get_arg("search_field"),search_value.strip(),session))
    await bot.send_private_msg(user_id=3453642726,message=event_list)


@join_event_command.handle()
async def handle(args: Message = CommandArg(),matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="actiId",message=args)


@join_event_command.got("actiId",prompt="请输入活动id")
async def handel(bot:Bot,matcher = Matcher,session: AsyncSession = Depends(get_session)):
    response = await pu.join_event(str(matcher.get_arg("actiId")).strip(),10,20,False,session)
    await bot.send_private_msg(user_id=3453642726,message=response)