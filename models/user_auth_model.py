from sqlalchemy import Column, Integer, String
from db.base import Base
from sqlalchemy.orm import relationship


class UserAuth(Base):
    __tablename__ = "user_auth"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    user_info = relationship("UserInfo", back_populates="user_auth", uselist=False)