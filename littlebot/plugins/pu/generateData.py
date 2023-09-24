import littlebot.plugins.pu.dao.eventListDao as eventListDao
import littlebot.plugins.pu.parseJsonDataUtil as parseJsonDataUtil


# 生成数据

# 生成活动列表
async def generate_event_list(session,event_list_contents=""):
    data = ""
    if event_list_contents:
        for event_list_content in event_list_contents:
            title = parseJsonDataUtil.get_data(event_list_content,"title")
            id = parseJsonDataUtil.get_data(event_list_content,"id")
            regStartTimeStr = parseJsonDataUtil.get_reg_start_time(event_list_content)
            regEndTimeStr = parseJsonDataUtil.get_reg_end_time(event_list_content)
            sTime = parseJsonDataUtil.get_data(event_list_content,"sTime")
            eTime = parseJsonDataUtil.get_data(event_list_content,"eTime")
            category = parseJsonDataUtil.get_data(event_list_content,"category")
            address = parseJsonDataUtil.get_data(event_list_content,"address")
            joinCount = parseJsonDataUtil.get_data(event_list_content,"joinCount")
            limitCount = parseJsonDataUtil.get_data(event_list_content,"limitCount")
            credit = parseJsonDataUtil.get_data(event_list_content,"credit")

            await eventListDao.insert_event_list(session,id=id, title=title, sTime=sTime, eTime=eTime, regStartTimeStr=regStartTimeStr, regEndTimeStr=regEndTimeStr,address=address,credit=credit,category=category,joinCount=joinCount,limitCount=limitCount)
            session.commit()
            data += f"""
            活动名称：{title}
            活动ID：{id}
            报名时间：{parseJsonDataUtil.format_time(regStartTimeStr)} ~ {parseJsonDataUtil.format_time(regEndTimeStr)}
            活动时间：{parseJsonDataUtil.format_time(sTime)} ~ {parseJsonDataUtil.format_time(eTime)}
            活动类型：{category}
            地点：{address}  人数：{joinCount}/{int(limitCount)+int(joinCount)}  分数：{credit}  
            """
    else:
        event_datas = await eventListDao.select_all(session)
        if not event_datas:
            return "error"
        for event_data in event_datas:
            title = event_data[0].title
            id = event_data[0].id
            regStartTimeStr = event_data[0].regStartTimeStr
            regEndTimeStr = event_data[0].regEndTimeStr
            sTime = event_data[0].sTime
            eTime = event_data[0].eTime
            category = event_data[0].category
            address = event_data[0].address
            joinCount = event_data[0].joinCount
            limitCount = event_data[0].limitCount
            credit = event_data[0].credit
            data += f"""
            活动名称：{title}
            活动ID：{id}
            报名时间：{parseJsonDataUtil.format_time(regStartTimeStr)} ~ {parseJsonDataUtil.format_time(regEndTimeStr)}
            活动时间：{parseJsonDataUtil.format_time(sTime)} ~ {parseJsonDataUtil.format_time(eTime)}
            活动类型：{category}
            地点：{address}  人数：{joinCount}/{int(limitCount) + int(joinCount)}  分数：{credit}  
            """
    return '\n'.join("    " + line.strip() for line in data.strip().split('\n'))


async def generate_filtered_event(search_field,search_value,session):
    event_data = ""
    data = ""
    match search_field:
        case "id":
            event_data = await eventListDao.select_event_by_id(session,search_value)
        case "category":
            event_data = await eventListDao.select_event_by_category(session,search_value)
        case "title":
            event_data = await eventListDao.select_event_by_title(session,search_value)
    if not event_data:
        return "error"

    if isinstance(event_data,list):
        print(1)
        for event_data in event_data:
            title = event_data[0].title
            id = event_data[0].id
            regStartTimeStr = event_data[0].regStartTimeStr
            regEndTimeStr = event_data[0].regEndTimeStr
            sTime = event_data[0].sTime
            eTime = event_data[0].eTime
            category = event_data[0].category
            address = event_data[0].address
            joinCount = event_data[0].joinCount
            limitCount = event_data[0].limitCount
            credit = event_data[0].credit
            data += f"""
            活动名称：{title}
            活动ID：{id}
            报名时间：{regStartTimeStr} ~ {regEndTimeStr}
            活动时间：{sTime} ~ {eTime}
            活动类型：{category}
            地点：{address}  人数：{joinCount}/{int(limitCount) + int(joinCount)}  分数：{credit}  
            """
    else:
        title = event_data.title
        id = event_data.id
        regStartTimeStr = event_data.regStartTimeStr
        regEndTimeStr = event_data.regEndTimeStr
        sTime = event_data.sTime
        eTime = event_data.eTime
        category = event_data.category
        address = event_data.address
        joinCount = event_data.joinCount
        limitCount = event_data.limitCount
        credit = event_data.credit
        data += f"""
        活动名称：{title}
        活动ID：{id}
        报名时间：{regStartTimeStr} ~ {regEndTimeStr}
        活动时间：{sTime} ~ {eTime}
        活动类型：{category}
        地点：{address}  人数：{joinCount}/{int(limitCount) + int(joinCount)}  分数：{credit}  
        """
    return '\n'.join("    " + line.strip() for line in data.strip().split('\n'))
