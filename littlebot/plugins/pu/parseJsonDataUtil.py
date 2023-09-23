import time
import littlebot.plugins.pu.requestsUtil as requestsUtil


def get_data(s, name):
    if "time" in name.lower():
        return format_time(s[name])
    return s[name]


def format_time(time_stamp):
    time_array = time.localtime(int(time_stamp))
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return formatted_time


def get_isAllowEvent(s):
    return True if s["isAllowEvent"] else False


def get_reg_start_time(s):
    detail = requestsUtil.requests_eventDetail(get_data(s, "id"))
    time_stamp = int(detail["content"]["regStartTimeStr"])
    time_array = time.localtime(time_stamp)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return formatted_time


def get_reg_end_time(s):
    detail = requestsUtil.requests_eventDetail(get_data(s, "id"))
    time_stamp = int(detail["content"]["regEndTimeStr"])
    time_array = time.localtime(time_stamp)
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return formatted_time
