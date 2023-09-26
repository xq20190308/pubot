import time
import littlebot.plugins.pu.requestsUtil as requestsUtil


def get_data(s, name):
    # if "time" in name.lower():
    #     return format_time(s[name])
    return s[name]


def format_time(time_stamp):
    time_array = time.localtime(int(time_stamp))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return formatted_time


def get_isAllowEvent(s):
    return True if s["isAllowEvent"] else False


def get_isJoin(user, s):
    detail = requestsUtil.requests_eventDetail(user, get_data(s, "id"))
    return True if int(detail["content"]["isJoin"]) == 2 else False


def get_allow_school(user, s):
    detail = requestsUtil.requests_eventDetail(user, get_data(s, "id"))
    allow_school = detail["content"]["allow_school"]
    return allow_school


def get_allow_year(user, s):
    detail = requestsUtil.requests_eventDetail(user, get_data(s, "id"))
    allow_year = detail["content"]["allow_year"]
    return allow_year


def get_reg_start_time(user, s):
    detail = requestsUtil.requests_eventDetail(user, get_data(s, "id"))
    time_stamp = detail["content"]["regStartTimeStr"]
    return time_stamp


def get_reg_end_time(user, s):
    detail = requestsUtil.requests_eventDetail(user, get_data(s, "id"))
    time_stamp = detail["content"]["regEndTimeStr"]
    return time_stamp
