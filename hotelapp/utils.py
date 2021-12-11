from hotelapp import app, db
from hotelapp.models import Kind, Room, User
from sqlalchemy import func
import hashlib


def load_kind():
    return Kind.query.all()


def load_room():
    return Room.query.filter(Room.active.__eq__(True))


def get_user_by_id(user_id):
    return User.query.get(user_id)

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())


        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

    return None

def room_count_by_cate():
    return Kind.query.join(Room,
                           Room.kind_id.__eq__(Kind.id), isouter=True)\
        .add_columns(func.count(Room.id)).group_by(Kind.id).all()