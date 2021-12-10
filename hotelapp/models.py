from datetime import datetime
from sqlalchemy import Column, Integer, String, Float,  Enum, DateTime, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from hotelapp import db
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default= datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

if __name__ == '__main__':
    pass
    #db.run(debug=True)
    #db.create_all()