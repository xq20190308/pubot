from sqlalchemy import select, delete
import littlebot.plugins.pu.dataModel as dataModel


# 定义模型

async def insert_event_list(session, id, title, category, address, joinCount, limitCount, credit, sTime, eTime,
                            regStartTimeStr,
                            regEndTimeStr):
    example = dataModel.EventList(id=int(id), title=title, category=category, address=address, joinCount=int(joinCount),
                                  limitCount=int(limitCount), credit=credit, sTime=sTime, eTime=eTime,
                                  regStartTimeStr=regStartTimeStr, regEndTimeStr=regEndTimeStr)
    session.add(example)
    await session.commit()


async def select_event_by_id(session, id):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.id == id))
    return stmt.scalar()


async def select_event_by_title(session, title):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.title == title))
    return stmt.scalar()


async def select_event_by_category(session, category):
    stmt = await session.execute(select(dataModel.EventList).where(dataModel.EventList.category == category))
    return stmt.fetchall()

async def select_all(session):
    stmt = await session.execute(select(dataModel.EventList))
    return stmt.fetchall()


async def delete_all(session):
    stmt = await session.execute(delete(dataModel.EventList))
    await stmt.commit()



# 因为 driver.on_startup 无法保证函数运行顺序
# 如需在 NoneBot 启动时且数据库初始化后运行的函数
# 请使用 post_db_init 而不是 Nonebot 的 on_startup
from nonebot_plugin_datastore.db import post_db_init


@post_db_init
async def do_something():
    pass
