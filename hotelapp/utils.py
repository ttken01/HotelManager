from hotelapp import app, db
from hotelapp.models import Kind, Room, User, Receipt, ReceiptDetail
from sqlalchemy import func
import hashlib

#lấy dữ liệu loại phòng
def load_kind():
    return Kind.query.all()

#lấy dữ liệu phòng
def load_room(kind = None, amount = None):

    rooms =  Room.query.filter(Room.active.__eq__(True))
    if kind:
        rooms = rooms.filter(Room.kind_id.__eq__(kind))
    if amount:
        rooms = rooms.filter(Room.amount.__eq__(amount))

    return rooms.all()


#lấy dữ liệu bill hóa đơn:
def load_receipt():

    return Receipt.query.all()

#lấy dữ liệu ReceiptDetail:
def load_ReceiptDetail():

    return ReceiptDetail.query.all()


#Trả về user theo Id
def get_user_by_id(user_id):
    return User.query.get(user_id)



#them user
def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name = name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar = kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()



#check account login có đúng không
def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())


        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

    return None


#đổ ra dữ liệu số phòng theo từng loại
def room_count_by_cate():
    return Kind.query.join(Room,
                           Room.kind_id.__eq__(Kind.id), isouter=True)\
        .add_columns(func.count(Room.id)).group_by(Kind.id).all()


def room_stats(kw=None, from_date=None, to_Date=None):
    p = db.session.query(Room.id, Room.name, func.sum())
    pass