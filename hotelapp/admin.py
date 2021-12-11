from hotelapp import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hotelapp.models import Kind, Room


admin = Admin(app=app, name="Hotel Website Administration", template_mode="bootstrap4")

class RoomView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price', 'amount', 'kind_id']
    column_exclude_list = ['image', 'active', 'created_date']
    column_labels = {
        'name': 'Tên SP',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Ảnh Phòng',
        'kind_id': 'Loại Phòng'
    }
    column_sortable_list = ['id', 'name', 'price']



admin.add_view(ModelView(Kind, db.session))
admin.add_view(RoomView(Room, db.session))