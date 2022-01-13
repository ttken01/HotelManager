from hotelapp import app, db
from hotelapp.models import Kind, Room, User, Receipt, ReceiptDetail, Comment, List
from sqlalchemy import func
from flask_login import current_user
from datetime import datetime
import hashlib

#lấy dữ liệu loại phòng
def load_kind():
    return Kind.query.all()



#lấy dữ liệu phòng
def load_room(kind = None, amount = None, from_date = None, to_date = None):

    rooms =  Room.query.filter(Room.active.__eq__(True))
    if kind:
        rooms = rooms.filter(Room.kind_id.__eq__(kind))
    if amount:
        rooms = rooms.filter(Room.amount.__eq__(amount))


    return rooms.all()

def get_room_by_id(room_id):
    return Room.query.get(room_id)

#lấy dữ liệu bill hóa đơn:
def load_receipt():

    return Receipt.query.all()

#lấy dữ liệu ReceiptDetail:
def load_ReceiptDetail():

    return ReceiptDetail.query.all()


#Trả về user theo Id
def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(user_name):
    return User.query.get(user_name)

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

#Them hang vao gio
def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    date_format = "%Y-%m-%d"

    if cart:
        for c in cart.values():
            check_in= datetime.strptime(c['check_in'], date_format)
            check_out= datetime.strptime(c['check_out'], date_format)
            delta = abs(check_in - check_out)
            c['days'] = delta.days + 1
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price'] * c['days']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

#Thêm đơn đặt phòng vao csdl

def add_receipt(cart):

    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              room_id=c['id'],
                              quantity=c['quantity'],
                              check_in = c['check_in'],
                              check_out = c['check_out'],
                              unit_price=c['price']*c['days'])
            db.session.add(d)

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


#Lọc dữ liệu bảng thông kê trên admin
def room_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(Room.id, Room.name, func.sum(ReceiptDetail.unit_price))\
                .join(ReceiptDetail, ReceiptDetail.room_id.__eq__(Room.id), isouter=True)\
                .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                .group_by(Room.id, Room.name)

    #xem doanh thu theo tên phòng
    if kw:
        p = p.filter(Room.name.contains(kw))

    #xuất ra doanh thu thông tin phòng từ ngày from_date
    if from_date:
        p = p.filter(ReceiptDetail.check_in.__ge__(from_date))

    #xem doanh thu những phòng trước ngày to_date
    if to_date:
        p = p.filter(ReceiptDetail.check_out.__le__(to_date))

    return p.all()

#Thống kê mật độ sử dụng phòng
def room_stats_used():
    p =  db.session.query(Room.name, func.count(Room.id))\
        .join(ReceiptDetail, ReceiptDetail.room_id.__eq__(Room.id), isouter = True) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
        .group_by(Room.name)

    return p.all()


def sum_rooms_stats():
    p = db.session.query(func.count(ReceiptDetail.receipt_id)) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))

    d=0
    for s in p:
        d = s[0]

    return d



def add_comment(content, room_id):
    c = Comment(content=content, room_id=room_id, user=current_user)

    db.session.add(c)
    db.session.commit()

    return c

def get_comments(page = 1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size

    return Comment.query.order_by(-Comment.id).slice(start, start + page_size).all()

#lấy dữ liệu phòng đẫ được đặt
def load_room_booking():
    q = db.session.query(
        User.name.label("username"),
        Room,
        Receipt,
        ReceiptDetail,
        List
    ).filter(ReceiptDetail.room_id ==Room.id)\
        .filter(Receipt.id==ReceiptDetail.receipt_id)\
        .filter( Receipt.user_id==User.id)
    return q.all()



#staff hủy phòng đẫ được đặt

#SELECT * FROM hotelapp.room as r, hotelapp.receipt as rc, hotelapp.receipt_detail as rcd where rc.id=1 && rc.id= rcd.receipt_id && rcd.room_id=r.id;
def room_booking_cancel(receipt_id):
    receipt = Receipt.query.filter(Receipt.id.__eq__(receipt_id)).first()

    p =  db.session.query(Room.name, func.count(Room.id))\
    .join(ReceiptDetail, ReceiptDetail.room_id.__eq__(Room.id), isouter = True) \
    .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
    .group_by(Room.name)


    db.session.delete(receipt)
    db.session.commit()