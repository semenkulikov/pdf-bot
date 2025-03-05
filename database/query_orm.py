from sqlalchemy.future import select
from database.models import User, Group
from database.engine import async_session

async def get_user_by_user_id(user_id: str):
    """ Получить пользователя по его id """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        return result.scalars().first()

async def create_user(user_id: str, full_name: str, username: str, is_premium: bool = None, is_subscribed=False):
    """ Создать объект пользователя """
    async with async_session() as session:
        user = User(user_id=user_id, full_name=full_name,
                    username=username, is_premium=is_premium,
                    is_subscribed=is_subscribed)
        session.add(user)
        await session.commit()
        return user

async def get_group_by_group_id(group_id: str):
    """ Получить группу по ее ID """
    async with async_session() as session:
        result = await session.execute(select(Group).where(Group.group_id == group_id))
        return result.scalars().first()

async def create_group(group_id: str, title: str, description: str = None, bio: str = None,
                       invite_link: str = None, location: str = None, username: str = None):
    """ Создать группу с заданными полями """
    async with async_session() as session:
        group = Group(
            group_id=group_id,
            title=title,
            description=description,
            bio=bio,
            invite_link=invite_link,
            location=location,
            username=username
        )
        session.add(group)
        await session.commit()
        return group

async def get_all_users():
    """ Получить всех пользователей """
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def set_is_subscribed(user_id: str, value: bool):
    """ Установить статус подписки пользователя на заданный """
    async with async_session() as session:
        user = await get_user_by_user_id(user_id)
        if user:
            user.is_subscribed = value
            await session.commit()
