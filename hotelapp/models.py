from datetime import datetime
from sqlalchemy import Column, Integer, String, Float,  Enum, DateTime, Boolean, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from hotelapp import db
from enum import Enum as UserEnum
from flask_login import UserMixin
import hashlib

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3

class User(BaseModel, UserMixin):
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

class Kind(BaseModel):
    __tablename__ = 'kind'

    name = Column(String(50), nullable=False)
    rooms = relationship('Room', backref='kind', lazy=True)

    def __str__(self):
        return self.name



class Room(BaseModel):
    __tablename__ = 'room'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    active = Column(Boolean, default=True)
    image = Column(String(100))
    amount = Column(Integer, default = 1)
    kind_id = Column(Integer, ForeignKey(Kind.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='room', lazy=True)

    def __str__(self):
        return self.name

class Receipt(BaseModel):
    start_date = Column(DateTime, default = datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    end_date = Column(DateTime, default = datetime.now())
    details = relationship('ReceiptDetail', backref='receipt', lazy=False)


class ReceiptDetail(BaseModel):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    paid = Column(Boolean, default=False)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
    #pass
    #db.run(debug=True)
    # k1 = Kind(name='Standard')
    # k2 = Kind(name='Superior')
    # k3 = Kind(name='Deluxe')
    # k4 = Kind(name='Suite')
    # db.session.add(k1)
    # db.session.add(k2)
    # db.session.add(k3)
    # db.session.add(k4)
    # db.session.commit()
    # password='123';
    # password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    # u1 = User(name='administrator', username= 'admin', password=password, user_role=UserRole.ADMIN )
    # db.session.add(u1)
    # db.session.commit()
    db.create_all()