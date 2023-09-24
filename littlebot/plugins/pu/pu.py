import json

import grequests

import littlebot.plugins.pu.dao.eventListDao as eventListDao
import littlebot.plugins.pu.generateData as generateData
import littlebot.plugins.pu.parseConfig as parseConfig


#获取活动列表
async def getEventList(page,session,force_flush=False):
    # print(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&page={page}")

    if force_flush:
        event_list = [grequests.get(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&page={page}")]
        event_list_res = grequests.map(event_list)[0]
        if not event_list_res.ok:
            return "获取列表失败"
        eventList = json.loads(event_list_res.text)
        if eventList["code"] != 0:
            return "权限不足，请检查token是否过期"
        if not eventList["content"]:
            return "无数据"
        if type(eventList) == 'str':
            return eventList
        await eventListDao.delete_all(session)
        return await generateData.generate_event_list(session,eventList["content"])

    else:
        res = await generateData.generate_event_list(session)
        if res == "error":
            res = await getEventList(page, session, True)
        return res


#过滤活动列表
async def get_filtered_event_list(search_field,search_value,session):
    res = await generateData.generate_filtered_event(search_field,search_value,session)
    if res == "error":
        return "未查找到活动数据，请检查输入值是否正确，若确认无误，则可尝试重新获取活动列表！"
    return res


async def join_event(actiId,size,single_requests_num,timer,session):
    event = await eventListDao.select_event_by_id(session, actiId)
    event_regStartTimeStr = event.regStartTimeStr
    event_regEndTimeStr = event.regEndTimeStr
    if timer:
        pass
    else:
        req_list = [grequests.get(
            parseConfig.url_eventJoin() + f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&id={actiId}")]
        res_list = grequests.map(req_list, size=size)[0]
        if not res_list.ok:
            return "报名失败"
        join_event:dict = json.loads(res_list.text)
        if not "msg" in join_event.keys():
            return "token过期"
        print(res_list.text)
        return json.loads(res_list.text)["msg"]