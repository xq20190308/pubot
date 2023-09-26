from sqlalchemy import select, delete, update, and_, or_
import littlebot.plugins.pu.dataModel as dataModel


# 定义模型

async def insert_event_list(session, id, title, category, address, joinCount, limitCount, credit, sTime, eTime,
                            allow_school, allow_year,
                            regStartTimeStr,
                            regEndTimeStr, eventStatus):
    example = dataModel.EventList(id=int(id), title=title, category=category, address=address, joinCount=int(joinCount),
                                  limitCount=int(limitCount), credit=credit, sTime=sTime, eTime=eTime,
                                  allow_school=allow_school, allow_year=allow_year,
                                  regStartTimeStr=regStartTimeStr, regEndTimeStr=regEndTimeStr,
                                  eventStatus=eventStatus)
    session.add(example)
    await session.commit()


async def select_event_by_id(session, id):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.id == id))
    return stmt.scalar()


async def select_event_by_eventStatus(session, eventStatus):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.eventStatus == eventStatus))
    return stmt.fetchall()


async def select_event_by_title(session, title):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.title == title))
    return stmt.scalar()


async def select_event_by_allow_school(session, allow_school):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.allow_school == allow_school))
    return stmt.fetchall()


async def select_event_by_allow_year(session, allow_year):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.allow_year == allow_year))
    return stmt.fetchall()


async def select_event_by_category(session, category):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.category == category))
    return stmt.fetchall()


async def select_event_by_isJoin(session, isJoin):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.isJoin == isJoin))
    return stmt.fetchall()


async def select_event_for_computer(session):
    stmt = await session.execute(select(dataModel.EventList).where(
        and_(or_(dataModel.EventList.allow_school == "全部",
                 dataModel.EventList.allow_school.like("%计算机科学与工程学院%")),
             or_(dataModel.EventList.allow_year == "全部", dataModel.EventList.allow_year == "%2022%"))))
    return stmt.fetchall()


async def select_all(session):
    stmt = await session.execute(select(dataModel.EventList))
    return stmt.fetchall()


async def delete_all(session):
    stmt = await session.execute(delete(dataModel.EventList))
    await session.commit()


async def update_event_by_id(session, id, isJoin):
    update_data = {
        dataModel.EventList.isJoin: isJoin  # 替换为要更新的列和新值
    }
    stmt = await session.execute(update(dataModel.EventList).where(dataModel.EventList.id == id).values(update_data))
    await session.commit()


# 因为 driver.on_startup 无法保证函数运行顺序
# 如需在 NoneBot 启动时且数据库初始化后运行的函数
# 请使用 post_db_init 而不是 Nonebot 的 on_startup
from nonebot_plugin_datastore.db import post_db_init


@post_db_init
async def do_something():
    pass
