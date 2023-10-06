from sqlalchemy import select, delete, update
import littlebot.plugins.pu.dataModel as dataModel


async def select_user_by_id(session, user_id):
    stmt = await session.execute(select(dataModel.Users).where(dataModel.Users.id == user_id))
    return stmt.scalar()

async def insert_user(session, user_id, email, password, oauth_token, oauth_token_secret,is_active):
    example = dataModel.Users(id=user_id,email=email,password=password,oauth_token=oauth_token,oauth_token_secret=oauth_token_secret,is_active=is_active)
    session.add(example)
    await session.commit()