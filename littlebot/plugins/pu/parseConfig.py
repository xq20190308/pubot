import yaml

with open("D:\\Documents\\qqbot\\nonebot\\littlebot\\littlebot\\plugins\\pu\\config.yaml", "r") as f:
    data = yaml.load(f, yaml.FullLoader)


def url_eventList():
    return data["url"]["eventList"]


def url_eventDetail():
    return data["url"]["eventDetail"]


def url_eventNotice():
    return data["url"]["eventNotice"]


def url_eventJoin():
    return data["url"]["eventJoin"]


def token_oauth_token():
    return data["token"]["oauth_token"]


def token_oauth_token_secret():
    return data["token"]["oauth_token_secret"]


def version():
    return data["version"]
