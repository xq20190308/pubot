import time

import requests
import json
import littlebot.plugins.pu.parseConfig as parseConfig

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"
}


def requests_login(email, password):
    res = requests.get(
        parseConfig.get_config(
            "eventLogin") + f"&email={email}&password={password}")

    res_login:dict = json.loads(res.text)
    print(res_login)
    if "message" in res_login.keys():
        return res_login["message"]
    if "userToken" not in res_login.keys():
        return "登录时发生未知错误！"

    return res_login["userToken"]


def requests_cancel_event(user, actiId):
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    res = requests.get(
        parseConfig.get_config(
            "eventCancel") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&id={actiId}")
    if not res.ok:
        return "取消报名失败，未知错误"
    if json.loads(res.text)["msg"] == "用户不存在":
        return "请检查活动id是否正确"
    return json.loads(res.text)["msg"]


def requests_sign(user, actiId, type):
    uid = user.uid
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    # res = requests.get(parseConfig.get_config("eventSign") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&actiId={actiId}&type={type}&userId={uid}")
    # if res.ok:
    #     return "TODO"
    return "TODO"


def requests_eventDetail(user, actiId):
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    event_list = requests.get(
        parseConfig.get_config(
            "eventDetail") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&version={parseConfig.get_config('version')}&actiId={actiId}")

    if not event_list.ok:
        return "获取列表失败"
    eventDetail = json.loads(event_list.text)
    if eventDetail["code"] != 0:
        return "权限不足，请检查token是否过期"
    if not eventDetail["content"]:
        return "无数据"
    return eventDetail

def requests_eventLists(user, page):
    oauth_token = user.oauth_token
    oauth_token_secret = user.oauth_token_secret
    res_event_lists = requests.get(
        parseConfig.get_config(
            "eventList") + f"&oauth_token={oauth_token}&oauth_token_secret={oauth_token_secret}&version={parseConfig.get_config('version')}&page={page}")
    if not res_event_lists.ok:
        return "error获取列表失败"
    eventList = json.loads(res_event_lists.text)
    if eventList["code"] != 0:
        return "error权限不足，请检查token是否过期"
    if not eventList["content"]:
        return "error无数据"
    if type(eventList) == 'str':
        return "error"+eventList
    return eventList
