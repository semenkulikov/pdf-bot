from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, nullable=False)  # Telegram ID
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    is_premium = Column(Boolean, nullable=True)
    is_subscribed = Column(Boolean, default=False)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    invite_link = Column(String, nullable=True)
    location = Column(String, nullable=True)
    username = Column(String, nullable=True)


class PDFCountry(Base):
    __tablename__ = 'pdf_countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)

    services = relationship("PDFService", back_populates="country", cascade="all, delete-orphan")


class PDFService(Base):
    __tablename__ = 'pdf_services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Например: "Leboncoin", "Ebay"
    country_id = Column(Integer, ForeignKey('pdf_countries.id'), nullable=False)

    # Дополнительные поля для шаблона PDF (будут расширяться в будущем)
    template_fields = Column(Text, nullable=True, comment="JSON с описанием полей шаблона")

    country = relationship("PDFCountry", back_populates="services")
