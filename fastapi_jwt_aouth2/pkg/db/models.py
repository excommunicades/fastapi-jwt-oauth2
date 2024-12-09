from sqlalchemy import Column, String, Integer

from fastapi_jwt_aouth2.pkg.db.database import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)

    nickname = Column(String(50), unique=True, nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)
