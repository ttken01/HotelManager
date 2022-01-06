from hotelapp import app, db, login
from flask import render_template, request, redirect, url_for, session
import utils
from flask_login import login_user, logout_user
from hotelapp.admin import *
import cloudinary.uploader

@app.route('/', methods = ['post', 'get'])
def home():
    rooms =None
    if request.method.__eq__('POST'):
        kind = request.form.get('kind')
        amount = request.form.get('amount')
        from_date = request.form.get('startdate')
        to_date = request.form.get('enddate')

        rooms = utils.load_room(kind=kind, amount=int(amount), from_date =from_date, to_date=to_date)
        return render_template('index.html', rooms=rooms)

    else: return render_template('index.html')

@app.route('/staff1', methods = ['post', 'get'])
def staff1():
    rooms = utils.load_room()
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        roomid = request.form.get('roomid')
        from_date = request.form.get('startdate')
        to_date = request.form.get('enddate')
        user = utils.get_user_by_username(user_name=username.strip())
        try:
                return redirect(url_for('staff1'))
        except Exception as ex:
            err_msg = 'He thong dang co loi:' + str(ex)

    return render_template('staff1.html', rooms=rooms)


@app.route('/register', methods = ['post', 'get'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('home'))
            else:
                err_msg = 'Mat khau KHONG khop!!!'
        except Exception as ex:
            err_msg = 'He thong dang co loi:' + str(ex)

    return render_template('register.html', err_msg=err_msg)


#ddang nhap nguoi dung
@app.route('/user-login', methods = ['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username= username, password = password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = 'Username or password INCORRECT'


    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.context_processor
def common_response():
    return {
        'kind': utils.load_kind(),
        'userRole' : UserRole
    }


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/admin-login', methods=['post'])
def admin_login():


    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login(username=username, password = password)

    if user:
        login_user(user=user)


    return redirect('/admin')


#@app.route('/api/ađ-cart', method=['post'])
#def add_to_cart():
    #id = ''
    #name = ''
    #price = ''

    #cart = session.get('cart')
    #if cart:
     #   cart = {}

    #pass


if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)