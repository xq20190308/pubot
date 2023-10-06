from typing import Tuple, Annotated

from nonebot import get_driver, require
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, Event
from nonebot.internal.matcher import Matcher
from nonebot.internal.params import ArgPlainText
from nonebot.params import CommandArg, Command, CommandStart, RawCommand
from nonebot.params import Depends
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_datastore import get_plugin_data, get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

import littlebot.plugins.pu.dataModel as dataModel
import littlebot.plugins.pu.generateData as generateData
import littlebot.plugins.pu.parseConfig as parseConfig
import littlebot.plugins.pu.pu
import littlebot.plugins.pu.dao.usersdao as usersdao
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


# 管理员权限
async def admin_permission(event: Event):
    if event.get_user_id() == parseConfig.get_config("admin_id"):
        return True
    return False


# async def user_permission(bot:Bot, event:Event):
#     user = await usersdao.select_user_by_id(session,event.get_user_id())
#     if user.is_active==1:
#         return True
#     else:
#         await bot.send_group_msg(group_id=parseConfig.get_config("group_id"),message=f"[CQ:at,qq={event.get_user_id()}]账号未激活，您无法使用该bot o(╥﹏╥)o")
#         return False
login_command = on_command("登录", rule=to_me(), priority=10, block=True)
help_command = on_command("帮助", rule=to_me(), priority=10, block=True)
get_event_list_command = on_command("获取活动列表", rule=to_me(), priority=10, block=True)
get_filtered_event_list_command = on_command("过滤活动列表", rule=to_me(), priority=10, block=True)
join_event_command = on_command("活动报名", rule=to_me(), priority=10, block=True)
cancel_event_command = on_command("取消报名", rule=to_me(), priority=10, block=True)
flush_timer_command = on_command(("列表自动刷新", "on"), rule=to_me(), aliases={("列表自动刷新", "off")}, priority=10,
                                 block=True, permission=admin_permission)
sign_command = on_command("签到", rule=to_me(), aliases={"签退"}, priority=10, block=True, permission=admin_permission)


@login_command.handle()
async def handel(args: Message = CommandArg(), matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="student_number", message=args)


@login_command.got("student_number", prompt="请输入学号")
async def handel(student_number: str = ArgPlainText(), matcher=Matcher):
    student_number = student_number.strip()
    if not student_number.isdigit():
        await login_command.reject(f"您输入的学号{student_number}不合法，请重新输入：")

@login_command.got("password", prompt="请输入密码")
async def _(bot:Bot,password: str = ArgPlainText(),matcher=Matcher,event=Event,session: AsyncSession = Depends(get_session)):
    user_id = event.get_user_id()
    email = matcher.get_arg("student_number") + "@" + parseConfig.get_config("school_email")
    password = password.strip()
    print(type(email))
    res = await pu.login(user_id=user_id,email=email.extract_plain_text(),password=password,session=session)
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"),message=f"[CQ:at,qq={user_id}]{res}")



@get_event_list_command.handle()
async def get_event_list_function(bot: Bot, event=Event, session: AsyncSession = Depends(get_session),
                                  args: Message = CommandArg()):
    force_flush_flag = False
    # user_info = await bot.get_login_info()
    user_id = event.get_user_id()
    if args.extract_plain_text():
        if "force_flush" in args.extract_plain_text():
            force_flush_flag = True
    event_list = generateData.check_type(await pu.getEventList(user_id, 4, session, force_flush_flag))
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=event_list)
    await session.commit()


@get_filtered_event_list_command.handle()
async def handel(args: Message = CommandArg(), matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="search_field", message=args)


@get_filtered_event_list_command.got("search_field", prompt="请输入过滤字段")
async def handel(search_field: str = ArgPlainText(), matcher=Matcher):
    search_field = search_field.strip()
    matcher.set_arg("search_field", search_field.strip())
    if search_field not in ["id", "title", "category", "isJoin", "group"]:
        await get_filtered_event_list_command.reject(f"你输入的{search_field}暂不支持检索，请重新输入")


@get_filtered_event_list_command.got("search_value", prompt="请输入过滤值")
async def handel2(bot: Bot, search_value: str = ArgPlainText(), matcher=Matcher,
                  session: AsyncSession = Depends(get_session)):
    event_list = generateData.check_type(
        await pu.get_filtered_event_list(matcher.get_arg("search_field"), search_value.strip(), session))
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=event_list)


@sign_command.handle()
async def _(bot: Bot, cmd: Annotated[tuple[str, ...], Command()], arg: Message = CommandArg(), event=Event,
            session: AsyncSession = Depends(get_session)):
    user_id = event.get_user_id()
    if cmd[0] == "签到":
        type = 1
    else:
        type = 2
    res = await pu.sign(user_id, arg.extract_plain_text(), type, session)
    await bot.send_private_msg(user_id=int(parseConfig.get_config("admin_id")), message=res)


@join_event_command.handle()
async def handle(args: Message = CommandArg(), matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="actiId", message=args)


@join_event_command.got("actiId", prompt="请输入活动id")
async def handel(bot: Bot, matcher=Matcher, session: AsyncSession = Depends(get_session), event=Event):
    user_id = event.get_user_id()
    response = await pu.join_event(user_id, str(matcher.get_arg("actiId")).strip(), bot, session)
    if response:
        await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=response)


@cancel_event_command.handle()
async def handle(args: Message = CommandArg(), matcher=Matcher):
    if args.extract_plain_text():
        matcher.set_arg(key="actiId", message=args)


@cancel_event_command.got("actiId", prompt="请输入活动id")
async def handel(bot: Bot, matcher=Matcher, session: AsyncSession = Depends(get_session), event=Event):
    user_id = event.get_user_id()
    response = await pu.cancel_event(user_id, str(matcher.get_arg("actiId")).strip(), session)
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=f"[CQ:at,qq={user_id}] " + response)


@flush_timer_command.handle()
async def handle(bot: Bot, cmd: Tuple[str, str] = Command(), event=Event, session: AsyncSession = Depends(get_session)):
    # action = arg.extract_plain_text()
    _, action = cmd
    print(action)
    match action:
        case "on":
            user_id = event.get_user_id()
            scheduler.add_job(
                pu.timer_flush,  # 指定要运行的函数
                "interval",
                minutes=30,
                id="flush_timer",
                args=(bot, user_id, 4, session)
            )
            res = "定时刷新开启成功"
        case "off":
            scheduler.remove_job(id="flush_timer")
            res = ("定时刷新关闭成功")
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=res)


@help_command.handle()
async def _(bot: Bot):
    message = """
    欢迎来到pu-bot ━(*｀∀´*)ノ亻!
    下面是本bot的使用命令
    /获取活动列表：获取活动列表
    /过滤活动列表：根据自己的需要输入字段，字段名如下：
        1. id：活动id
        2. title：活动标题
        3. category：活动分类
        4. group：特定分组
    /活动报名：报名活动，若为到报名时间，则自动设置为定时报名
    /取消报名：取消报名活动
    """
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=message)
