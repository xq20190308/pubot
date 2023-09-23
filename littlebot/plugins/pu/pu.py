import json
import requests
import littlebot.plugins.pu.parseConfig as parseConfig
import littlebot.plugins.pu.generateData as generateData
import littlebot.plugins.pu.requestsUtil as requestsUtil

async def getEventList(page,session,force_flush=False):
    # print(parseConfig.url_eventList()+f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&page={page}")

    if force_flush:
        eventList = requestsUtil.requests_eventList(page)
        if type(eventList) == 'str':
            return eventList
        return await generateData.generate_event_list(session,eventList["content"])

    else:
        res = await generateData.generate_event_list(session)
        if res == "error":
            res = await getEventList(page, session, True)
        return res

async def get_filtered_event_list(search_field,search_value,session):
    print(search_field+":"+search_value)
    res = await generateData.generate_filtered_event(search_field,search_value,session)
    if res == "error":
        return "未查找到活动数据，请检查输入值是否正确，若确定正确，则可尝试先重新获取活动列表！"
    return res