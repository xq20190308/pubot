import time

import requests
import json
import littlebot.plugins.pu.parseConfig as parseConfig

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41"
}



def requests_eventDetail(actiId):
    event_list = requests.get(
        parseConfig.url_eventDetail() + f"&oauth_token={parseConfig.token_oauth_token()}&oauth_token_secret={parseConfig.token_oauth_token_secret()}&version={parseConfig.version()}&actiId={actiId}")

    if not event_list.ok:
        return "获取列表失败"
    eventDetail = json.loads(event_list.text)
    if eventDetail["code"] != 0:
        return "权限不足，请检查token是否过期"
    if not eventDetail["content"]:
        return "无数据"
    return eventDetail


