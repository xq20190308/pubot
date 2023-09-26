import base64
import io

from PIL import Image, ImageDraw, ImageFont
import filetype

import littlebot.plugins.pu.dao.eventListDao as eventListDao
import littlebot.plugins.pu.parseJsonDataUtil as parseJsonDataUtil


# 生成数据

# 生成活动列表
async def generate_event_list(session, user, event_list_contents=""):
    data = ""
    if event_list_contents:
        for event_list_content in event_list_contents:
            eventStatus = parseJsonDataUtil.get_data(event_list_content, "eventStatus")
            if eventStatus != 3 and eventStatus != 4:
                continue

            title = parseJsonDataUtil.get_data(event_list_content, "title")
            id = parseJsonDataUtil.get_data(event_list_content, "id")
            regStartTimeStr = parseJsonDataUtil.get_reg_start_time(user, event_list_content)
            regEndTimeStr = parseJsonDataUtil.get_reg_end_time(user, event_list_content)
            allow_school = parseJsonDataUtil.get_allow_school(user, event_list_content)
            allow_school = "全部" if len(allow_school) != 1 else allow_school[0]
            allow_year = parseJsonDataUtil.get_allow_year(user, event_list_content)
            allow_year = "，".join([str(item) for item in allow_year]) if len(allow_year) > 0 else "全部"
            sTime = parseJsonDataUtil.get_data(event_list_content, "sTime")
            eTime = parseJsonDataUtil.get_data(event_list_content, "eTime")
            category = parseJsonDataUtil.get_data(event_list_content, "category")
            address = parseJsonDataUtil.get_data(event_list_content, "address")
            joinCount = parseJsonDataUtil.get_data(event_list_content, "joinCount")
            limitCount = parseJsonDataUtil.get_data(event_list_content, "limitCount")
            credit = parseJsonDataUtil.get_data(event_list_content, "credit")

            await eventListDao.insert_event_list(session, id=id, title=title, sTime=sTime, eTime=eTime,
                                                 regStartTimeStr=regStartTimeStr, regEndTimeStr=regEndTimeStr,
                                                 allow_school=allow_school, allow_year=allow_year,
                                                 address=address, credit=credit, category=category, joinCount=joinCount,
                                                 limitCount=limitCount, eventStatus=int(eventStatus))
            session.commit()
            data += template_text(title, id, regStartTimeStr, regEndTimeStr, sTime, eTime, category, allow_school,
                                  allow_year, address,
                                  joinCount, limitCount, credit, eventStatus)
    else:
        event_datas = await eventListDao.select_all(session)
        if not event_datas:
            return "error"
        for event_data in event_datas:
            title = event_data[0].title
            id = event_data[0].id
            regStartTimeStr = event_data[0].regStartTimeStr
            regEndTimeStr = event_data[0].regEndTimeStr
            allow_school = event_data[0].allow_school
            allow_year = event_data[0].allow_year
            sTime = event_data[0].sTime
            eTime = event_data[0].eTime
            category = event_data[0].category
            address = event_data[0].address
            joinCount = event_data[0].joinCount
            limitCount = event_data[0].limitCount
            credit = event_data[0].credit
            eventStatus = event_data[0].eventStatus
            data += template_text(title, id, regStartTimeStr, regEndTimeStr, sTime, eTime, category, allow_school,
                                  allow_year, address,
                                  joinCount, limitCount, credit, eventStatus)
    return '\n'.join("    " + line.strip() for line in data.strip().split('\n'))


async def generate_filtered_event(search_field, search_value, session):
    event_data = ""
    data = ""
    match search_field:
        case "id":
            event_data = await eventListDao.select_event_by_id(session, search_value)
        case "category":
            event_data = await eventListDao.select_event_by_category(session, search_value)
        case "title":
            event_data = await eventListDao.select_event_by_title(session, search_value)
        case "eventStatus":
            event_data = await eventListDao.select_event_by_eventStatus(session, search_value)
        case "group":
            event_data = await eventListDao.select_event_for_computer(session)
    if not event_data:
        return "error"

    if isinstance(event_data, list):
        for event_data in event_data:
            title = event_data[0].title
            id = event_data[0].id
            regStartTimeStr = event_data[0].regStartTimeStr
            regEndTimeStr = event_data[0].regEndTimeStr
            allow_school = event_data[0].allow_school
            allow_year = event_data[0].allow_year
            sTime = event_data[0].sTime
            eTime = event_data[0].eTime
            category = event_data[0].category
            address = event_data[0].address
            joinCount = event_data[0].joinCount
            limitCount = event_data[0].limitCount
            credit = event_data[0].credit
            eventStatus = event_data[0].eventStatus
            data += template_text(title, id, regStartTimeStr, regEndTimeStr, sTime, eTime, category, allow_school,
                                  allow_year, address,
                                  joinCount, limitCount, credit, eventStatus)
    else:
        title = event_data.title
        id = event_data.id
        regStartTimeStr = event_data.regStartTimeStr
        regEndTimeStr = event_data.regEndTimeStr
        allow_school = event_data.allow_school
        allow_year = event_data.allow_year
        sTime = event_data.sTime
        eTime = event_data.eTime
        category = event_data.category
        address = event_data.address
        joinCount = event_data.joinCount
        limitCount = event_data.limitCount
        credit = event_data.credit
        eventStatus = event_data.eventStatus
        data += template_text(title, id, regStartTimeStr, regEndTimeStr, sTime, eTime, category, allow_school,
                              allow_year, address,
                              joinCount, limitCount, credit, eventStatus)
    return '\n'.join("    " + line.strip() for line in data.strip().split('\n'))


def template_text(title, id, regStartTimeStr, regEndTimeStr, sTime, eTime, category, allow_school, allow_year, address,
                  joinCount, limitCount, credit, eventStatus):
    return f"""
        活动名称：{title}（{"未开始" if eventStatus == 3 else "进行中" if eventStatus == 4 else "已结束"}）
        活动ID：{id}
        报名时间：{parseJsonDataUtil.format_time(regStartTimeStr)} ~ {parseJsonDataUtil.format_time(regEndTimeStr)}
        活动时间：{parseJsonDataUtil.format_time(sTime)} ~ {parseJsonDataUtil.format_time(eTime)}
        活动类型：{category}
        活动院系：{allow_school}  活动年级：{allow_year}
        地点：{address}  人数：{joinCount}/{"∞" if int(limitCount) + int(joinCount) > 600000 else int(limitCount) + int(joinCount)}  分数：{credit}
        """


def generate_pic(text):
    if isinstance(text, bytes) or len(text) <= 20:
        return text
    # 选择字体和文字颜色
    font_size = 20
    font_color = (0, 0, 0)  # 黑色
    font = ImageFont.truetype('D:\\msyh.ttc', font_size)
    # 计算文本的行数
    text_lines = text.split('\n')
    line_height = font.getbbox(text_lines[0])[3]
    num_lines = len(text_lines)

    # 计算图片高度
    height = num_lines * line_height

    # 创建图像
    width = 900
    background_color = (255, 255, 255)  # 白色
    image = Image.new('RGB', (width, height), background_color)

    # 创建一个绘图对象
    draw = ImageDraw.Draw(image)

    # 在图像上绘制文本
    text_x, text_y = 0, 0
    for line in text_lines:
        draw.text((text_x, text_y), line, font=font, fill=font_color)
        text_y += line_height

    buffer = io.BytesIO()
    image.save(buffer, "JPEG")
    return buffer.getvalue()


def check_type(data):
    if not isinstance(data, str):
        file_type = filetype.guess(data)
        if file_type.mime == "image/jpeg" or file_type.mime == "image/png":
            return f"[CQ:image,file=base64://{base64.b64encode(data).decode()}]"
    return data
