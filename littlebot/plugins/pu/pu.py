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


# 获取活动列表
async def getEventList(user_id, page, session, force_flush=False):
    # print(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&page={page}")
    user_info = await usersdao.select_user_by_id(session, user_id)
    oauth_token = user_info.oauth_token
    oauth_token_secret = user_info.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret)
    if force_flush:
        all_event_list = ""
        await eventListDao.delete_all(session)
        for i in range(page):

            # event_list = requests.get(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&page={i}")
            # res_event_lists = grequests.map(event_list)

            res_event_lists = requests.get(
                parseConfig.get_config("eventList") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&version={parseConfig.get_config('version')}&page={i + 1}")
            if not res_event_lists.ok:
                return "获取列表失败"
            eventList = json.loads(res_event_lists.text)
            if eventList["code"] != 0:
                return "权限不足，请检查token是否过期"
            if not eventList["content"]:
                return "无数据"
            if type(eventList) == 'str':
                return eventList
            all_event_list += await generateData.generate_event_list(session, user, eventList["content"])
            all_event_list += "\n\n"

    else:
        all_event_list = await generateData.generate_event_list(session, user)
        if all_event_list == "error":
            all_event_list = await getEventList(user_id, page, session, True)
    return generateData.generate_pic(all_event_list)


# 过滤活动列表
async def get_filtered_event_list(search_field, search_value, session):
    res = await generateData.generate_filtered_event(search_field, search_value, session)
    if res == "error":
        return "未查找到活动数据，请检查输入值是否正确，若确认无误，则可尝试重新获取活动列表！"
    return generateData.generate_pic(res)


async def join_event(user_id, actiId, timer, bot, session):
    event = await eventListDao.select_event_by_id(session, actiId)
    user_info = await usersdao.select_user_by_id(session, user_id)
    oauth_token = user_info.oauth_token
    oauth_token_secret = user_info.oauth_token_secret
    user = User(user_id, oauth_token, oauth_token_secret)
    event_regStartTime = float(event.regStartTimeStr)
    current_time = time.time()

    if event_regStartTime - current_time > 10:
        event_regStartTime = datetime.fromtimestamp(event_regStartTime)  # 转换为 datetime 对象
        print(event_regStartTime)
        scheduler.add_job(
            timer_join,  # 指定要运行的函数
            user,
            "date",  # 定时任务类型，这里使用 "date" 表示一次性定时任务
            next_run_time=event_regStartTime,  # 传递 datetime 对象作为下次运行的时间
            args=(bot, session, actiId),  # 传递给函数的参数，使用元组
        )
        return f"未达到活动报名时间，将于 {event_regStartTime.strftime('%Y-%m-%d %H:%M:%S')} 自动签到"
    else:
        res_list = requests.get(
            parseConfig.get_config("eventJoin") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&id={actiId}")
        # res_list = grequests.map(req_list, size=size)[0]

        if not res_list.ok:
            return "报名失败，未知原因"
        join_event: dict = json.loads(res_list.text)
        if not "msg" in join_event.keys():
            return "token过期"
        print(res_list.text)
        return json.loads(res_list.text)["msg"]


# 定时报名任务
async def timer_join(bot: Bot, user, session, actiId):
    result = ""
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    res_list = requests.get(
        parseConfig.get_config('eventJoin') + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&id={actiId}")
    if not res_list.ok:
        result = "报名失败，未知原因"
    result = json.loads(res_list.text)["msg"]
    await bot.send_private_msg(user_id=3453642726, message=result)
    # await eventListDao.update_event_by_id(session,actiId,isJoin)
