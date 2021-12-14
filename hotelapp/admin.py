from hotelapp import app, db, utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hotelapp.models import Kind, Room, User, UserRole
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request



# Đăng nhập với tư cách admin
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN



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


#bắt đăng nhập mới hiện trang dữ liệu
class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedBaseView):

    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')


#Trang mới: Thống kê báo cáo
class StatsView(BaseView):

    @expose('/')
    def __index__(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        return self.render('admin/stats.html', stats=utils.room_stats(kw=kw,
                                                                      from_date=from_date,
                                                                      to_date=to_date))

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

admin.add_view(AuthenticatedModelView(Kind, db.session, name='Loại phòng'))
admin.add_view(RoomView(Room, db.session, name='Phòng'))
admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))