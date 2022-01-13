from datetime import datetime
from sqlalchemy import Column, Integer, String, Float,  Enum, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from hotelapp import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

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
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy =True)

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
    comments = relationship('Comment', backref='room', lazy=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content



class Receipt(BaseModel):
    created_date = Column(DateTime, default = datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False, primary_key=True)
    check_in = Column(DateTime, default= datetime.now())
    check_out = Column(DateTime, default= datetime.now())
    quantity = Column(Integer , default=0)
    paid = Column(Boolean, default=False)
    unit_price = Column(Float, default=0)



class KindGuest(UserEnum):
    LOCAL = 1
    FOREIGN = 2




class List(BaseModel):
    receipt_id = Column(Integer, ForeignKey(ReceiptDetail.receipt_id), nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)
    kind_guest = Column(Enum(KindGuest), default=KindGuest.LOCAL)
    cmnd = Column(String(30), nullable=False)
    address = Column(String(100))
    receipt_details = relationship('ReceiptDetail', backref='list', lazy=True)




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
    # u2 = User(name='staff', username= 'staff', password=password, user_role=UserRole.STAFF )
    # us1 = User(name='us1', username= 'us1', password=password, user_role=UserRole.USER )
    # db.session.add(u1)
    # db.session.add(u2)
    # db.session.add(us1)
    # db.session.commit()
    # r1 = Receipt(user_id=us1.id, details=[ReceiptDetail(room_id=1, check_in=datetime.now(), check_out=datetime.now(), quantity=1, paid=False, unit_price=0)])
    # db.session.add(r1)
    # db.session.commit()
    l1 = List(receipt_id=1, name="us1", kind_guest=KindGuest.FOREIGN, cmnd='123456789', address='123')
    db.session.add(l1)
    db.session.commit()
    db.create_all()