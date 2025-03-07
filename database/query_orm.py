from sqlalchemy.future import select
from database.models import User, Group, PDFService, PDFCountry
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

async def get_all_pdf_countries():
    async with async_session() as session:
        result = await session.execute(select(PDFCountry))
        return result.scalars().all()

async def get_pdf_country_by_code(code: str):
    async with async_session() as session:
        result = await session.execute(select(PDFCountry).where(PDFCountry.code == code))
        return result.scalars().first()

async def create_pdf_country(name: str, code: str):
    async with async_session() as session:
        country = PDFCountry(name=name, code=code)
        session.add(country)
        await session.commit()
        return country

async def get_pdf_services_by_country_id(country_id: int):
    async with async_session() as session:
        result = await session.execute(select(PDFService).where(PDFService.country_id == country_id))
        return result.scalars().all()

async def get_pdf_service_by_id(service_id: int):
    async with async_session() as session:
        result = await session.execute(select(PDFService).where(PDFService.id == service_id))
        return result.scalars().first()

async def create_pdf_service(name: str, country_id: int, template_fields: str = None):
    async with async_session() as session:
        service = PDFService(name=name, country_id=country_id, template_fields=template_fields)
        session.add(service)
        await session.commit()
        return service
