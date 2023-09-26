from sqlalchemy import select, delete, update
import littlebot.plugins.pu.dataModel as dataModel


async def select_user_by_id(session, user_id):
    stmt = await session.execute(select(dataModel.Users).where(dataModel.Users.id == user_id))
    return stmt.scalar()
