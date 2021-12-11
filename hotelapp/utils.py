from hotelapp import app, db
from hotelapp.models import Kind, Room, User
import hashlib


def load_kind():
    return Kind.query.all()


def load_room():
    return Room.query.filter(Room.active.__eq__(True))




