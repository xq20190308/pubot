import requests
import json
import littlebot.plugins.pu.parseConfig as parseConfig


def requests_eventList(page):
    eventListResponse = requests.get(
        parseConfig.url_eventList() + f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&page={page}")
    if not eventListResponse.ok:
        return "获取列表失败"
    eventList = json.loads(eventListResponse.text)
    if eventList["code"] != 0:
        return "权限不足，请检查token是否过期"
    if not eventList["content"]:
        return "无数据"
    return eventList


def requests_eventDetail(actiId):
    eventDetailResponse = requests.get(
        parseConfig.url_eventDetail() + f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&actiId={actiId}")
    if not eventDetailResponse.ok:
        return "获取列表失败"
    eventDetail = json.loads(eventDetailResponse.text)
    if eventDetail["code"] != 0:
        return "权限不足，请检查token是否过期"
    if not eventDetail["content"]:
        return "无数据"
    return eventDetail
