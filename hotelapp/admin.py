from hotelapp import app, db, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hotelapp.models import Kind, Room, User, UserRole, Comment, Receipt, ReceiptDetail, List
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request



# Đăng nhập với tư cách admin
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ReceiptView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    can_create = False
    can_edit = False
    column_labels = {
        'user' : 'Khách hàng',
        'content' : 'Bình luận',
        'created_date' : 'Ngày tạo',
        'check_in' : 'Ngày nhận phòng',
        'check_out' : 'Ngày trả phòng',
        'paid' : 'Thanh toán',
        'unit_price': 'Tổng hóa đơn',
        'room_id': 'Phòng',
        'receipt_id': 'Hóa đơn',
        'name': 'Tên thành viên',
        'kind_guest': 'Loại khách hàng',
        'cmnd': 'Chứng minh nhân dân',
        'address': 'Địa chỉ'
    }


class CommentView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['content', 'user_id', 'room_id']
    column_filters = ['room_id']
    column_sortable_list = ['id', 'room_id']
    column_labels = {
        'content' : 'Bình luận',
        'created_date' : 'Ngày tạo',
        'user_id' : 'Khách hàng',
        'room_id' : 'Phòng'
    }


class RoomView(AuthenticatedModelView):
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

class UserView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_filters = ['name', 'username']
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['avatar', 'active', 'joined_date']


#bắt đăng nhập mới hiện trang dữ liệu
class AuthenticatedBaseView(BaseView):
    def is_accessible(self):

        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):

    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/')


#Trang mới: Thống kê báo cáo
class StatsView(BaseView):

    @expose('/')
    def __index__(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        stats = utils.room_stats(kw=kw,
                                 from_date=from_date,
                                 to_date=to_date)
        stats_sum = 0
        for s in stats:
            stats_sum += s[2]

        return self.render('admin/stats.html', stats=stats, stats_sum=stats_sum , statsUsed=utils.room_stats_used(),
                                                                        sumUsed=utils.sum_rooms_stats())

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN



#xử lý thống kê Home Admin
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def __index__(self):
        stats = utils.room_count_by_cate()

        return self.render('admin/index.html', stats=stats)






admin = Admin(app=app,
              name="Hotel Website Administration",
              template_mode="bootstrap4",
              index_view=MyAdminIndexView())

admin.add_view(AuthenticatedModelView(Kind, db.session, name='Loại Phòng'))
admin.add_view(RoomView(Room, db.session, name='Phòng'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(CommentView(Comment, db.session, name='Bình luận' ))
admin.add_view(ReceiptView(Receipt, db.session, name='Hóa đơn'))
admin.add_view(ReceiptView(ReceiptDetail, db.session, name='Chi tiết HĐ'))
admin.add_view(ReceiptView(List, db.session, name='Room Members'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))