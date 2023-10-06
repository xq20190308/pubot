import json
import time
from datetime import datetime
import requests
from nonebot import require
import littlebot.plugins.pu.dao.eventListDao as eventListDao
import littlebot.plugins.pu.dao.usersdao as usersdao
import littlebot.plugins.pu.generateData as generateData
import littlebot.plugins.pu.parseConfig as parseConfig
from littlebot.plugins.pu.User import User
from nonebot.adapters.onebot.v11 import Bot

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
import littlebot.plugins.pu.requestsUtil as requestsUtil


async def login(user_id, email, password, session):
    user_info = await usersdao.select_user_by_id(session, user_id)
    if user_info:
        oauth_token = user_info.oauth_token
        oauth_token_secret = user_info.oauth_token_secret
        user = User(user_id, oauth_token, oauth_token_secret)
        res_test = requestsUtil.requests_eventLists(user, 1)
        if not (isinstance(res_test, str) and res_test[0:5] == "error"):
            return "登陆成功"
    # 数据库中没有该用户信息，或者token过期
    res_login = requestsUtil.requests_login(email, password)
    if isinstance(res_login,dict) and res_login["oauth_token"] and res_login["oauth_token_secret"]:
        print(type(email))
        await usersdao.insert_user(session=session,user_id=user_id, email=email, password=password,
                                   oauth_token=res_login["oauth_token"],
                                   oauth_token_secret=res_login["oauth_token_secret"], is_active=1)
        return "登录成功"
    return res_login


# 获取活动列表
async def getEventList(user_id, page, session, force_flush=False, flush_timer=False):
    # print(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&page={page}")
    user_info = await usersdao.select_user_by_id(session, user_id)
    if not user_info:
        return '未找到该用户信息，请先输入"/登录"'
    oauth_token = user_info.oauth_token
    oauth_token_secret = user_info.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret)
    if force_flush:
        all_event_list = ""
        await eventListDao.delete_all(session)
        for i in range(page):

            # event_list = requests.get(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&page={i}")
            # res_event_lists = grequests.map(event_list)

            event_list = requestsUtil.requests_eventLists(user, i + 1)
            if isinstance(event_list, str) and event_list[0:5] == "error":
                return event_list[5:]
            all_event_list += await generateData.generate_event_list(session, user, event_list["content"])
            all_event_list += "\n\n"

    else:
        all_event_list = await generateData.generate_event_list(session, user)
        if all_event_list == "error":
            all_event_list = await getEventList(user_id, page, session, True)
    if flush_timer:
        return "ok"
    return generateData.generate_pic(all_event_list)


# 过滤活动列表
async def get_filtered_event_list(search_field, search_value, session):
    res = await generateData.generate_filtered_event(search_field, search_value, session)
    if res == "error":
        return "未查找到活动数据，请检查输入值是否正确，若确认无误，则可尝试重新获取活动列表！"
    return generateData.generate_pic(res)


async def join_event(user_id, actiId, bot, session):
    event = await eventListDao.select_event_by_id(session, actiId)
    if not event:
        return "数据库中未查到该活动，请尝试先获取活动列表！"
    user_info = await usersdao.select_user_by_id(session, user_id)
    oauth_token = user_info.oauth_token
    oauth_token_secret = user_info.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret)
    event_regStartTime = float(event.regStartTimeStr)
    event_regEndTime = float(event.regEndTimeStr)
    current_time = time.time()
    res = ""
    is_past = True
    if (current_time < event_regStartTime):
        is_past = False
        res = f"未达到活动报名时间，将于 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(event_regStartTime))} 自动签到"
    event_regStartTime = datetime.fromtimestamp(event_regStartTime)  # 转换为 datetime 对象
    if is_past:
        await timer_join(bot, user, session, actiId)
    else:
        scheduler.add_job(
            timer_join,  # 指定要运行的函数
            "date",  # 定时任务类型，这里使用 "date" 表示一次性定时任务
            next_run_time=event_regStartTime,  # 传递 datetime 对象作为下次运行的时间
            args=(bot, user, session, actiId),  # 传递给函数的参数，使用元组
        )
        return res


async def cancel_event(user_id, actiId, session):
    user_info = await usersdao.select_user_by_id(session, user_id)
    if not user_info:
        return '未找到该用户信息，请先输入"/登录"'
    oauth_token = user_info.oauth_token
    oauth_token_secret = user_info.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret)
    res = requestsUtil.requests_cancel_event(user, actiId)
    return res


async def sign(user_id, actiId, type, session):
    user = await usersdao.select_user_by_id(session, user_id)
    if not user_info:
        return '未找到该用户信息，请先输入"/登录"'
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    uid = user.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret, uid)
    return requestsUtil.requests_sign(user, actiId, type)


async def timer_flush(bot, user_id, page, session):
    res = await getEventList(user_id, page, session, True, True)
    if res == "ok":
        res = "刷新成功"
    await bot.send_private_msg(user_id=int(parseConfig.get_config("admin_id")), message=res)


# 定时报名任务
async def timer_join(bot: Bot, user, session, actiId):
    result = f"[CQ:at,qq={int(user.user_id)}] 活动id：{actiId} "
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    res_list = requests.get(
        parseConfig.get_config(
            'eventJoin') + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&id={actiId}")
    if not res_list.ok:
        result += "报名失败，未知原因"
    result += json.loads(res_list.text)['msg']
    print(result)
    await bot.send_group_msg(group_id=parseConfig.get_config("group_id"), message=result)
    # await eventListDao.update_event_by_id(session,actiId,isJoin)
