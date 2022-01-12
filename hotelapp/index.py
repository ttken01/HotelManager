from hotelapp import app, db, login
from flask import render_template, request, redirect, url_for, session, jsonify
import utils
from flask_login import login_user, logout_user, login_required
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
        if kind == '':
            if amount == '':
                rooms = utils.load_room(from_date=from_date, to_date=to_date)
            else:
                rooms = utils.load_room(amount=amount , from_date=from_date, to_date=to_date)
        if amount == '':
            if kind == '':
                rooms = utils.load_room(from_date=from_date, to_date=to_date)
            else:
                rooms = utils.load_room( kind=kind ,from_date=from_date, to_date=to_date)
        else:
            rooms = utils.load_room(kind=kind, amount=amount, from_date=from_date, to_date=to_date)
        return render_template('index.html', rooms=rooms)

    else: return render_template('index.html', rooms=utils.load_room())

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

            return redirect(url_for(request.args.get('next', 'index')))
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
        'userRole' : UserRole,
        'cart_stats': utils.cart_stats(session.get('cart'))
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

@app.route('/cart')
def cart():
    return render_template('cart.html',
                           cart_stats=utils.cart_stats(session.get('cart')))


@app.route('/api/add-to-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    check_in = data.get('check_in')
    check_out = data.get('check_out')


    cart = session.get('cart')

    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'check_in': check_in,
            'check_out': check_out,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.cart_stats(session.get('cart')))

@app.route('/api/update-cart', methods=['put'])
def update_cart():
    id = str(request.json.get('id'))
    quantity = request.json.get('quantity')

    cart = session.get('cart')
    err_msg = ''
    if cart:
        if id in cart:
            cart[id]['quantity'] = quantity
            session['cart'] = cart

            return jsonify({
                'code': 200,
                'data': utils.cart_stats(cart)
            })
        else:
            err_msg = 'Khong co san pham tuong ung de cap nhat!'
    else:
        err_msg = 'Chua co gio hang!'

    return jsonify({
        'code': 404,
        'err_msg': err_msg
    })


@app.route('/api/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    err_msg = ''
    if cart:
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart

            return jsonify({
                'code': 200,
                'data': utils.cart_stats(cart)
            })
        else:
            err_msg = 'Khong co san pham tuong ung de cap nhat!'
    else:
        err_msg = 'Chua co gio hang!'

    return jsonify({
        'code': 404,
        'err_msg': err_msg
    })

@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})


if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)