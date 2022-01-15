import string

from sqlalchemy.sql.elements import Null

from datetime import datetime
from hotelapp import app, db, login
from flask import render_template, request, redirect, url_for, session, jsonify, abort
from hotelapp.utils import booking_pay_by_id, room_booking_cancel
import utils
from flask_login import login_user, logout_user, login_required, current_user
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
@login_required
def staff1():
    if current_user.user_role == UserRole.STAFF:
        rooms = utils.load_room()
        err_msg = ""
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            roomid = request.form.get('roomid')
            from_date = request.form.get('startdate')
            to_date = request.form.get('enddate')
            amount = request.form.get('amount')
            arr = [[]]
            if from_date or to_date:
              from_date = datetime.strptime(from_date, "%Y-%m-%d")
              to_date = datetime.strptime(to_date, "%Y-%m-%d" )
            else:
              from_date = datetime.now()
              to_date = datetime.now()
           
            name = 'name'
            cmnd = 'cmnd'
            address = 'address'
            if username == "":
              user = current_user
            else:
              user = utils.get_user_by_username(user_name=username)
            if roomid == "":
              roomid = "1";
            if amount:
                for i in range(int(amount)):
                    print(i)
                    arr[i].append(request.form.get(name+ str(i)))
                    arr[i].append(request.form.get(cmnd+ str(i)))
                    arr[i].append(request.form.get(address+ str(i)))
                    utils.add_receipt_detail_list(user=user,
                                                room_id=roomid.strip(),
                                                check_in=from_date,
                                                check_out=to_date,
                                                amount=int(amount),
                                                arr=arr)
            else:
                utils.add_receipt_detail_list(user=user,
                                          room_id=roomid.strip(),
                                          check_in=from_date,
                                          check_out=to_date,
                                          amount=0)
            try:
                return redirect(url_for('staff1'))
            except Exception as ex:
             err_msg = 'He thong dang co loi:' + str(ex)


        return render_template('booking.html', rooms=rooms, err_msg=err_msg)
    else:
        abort(403)  

  

@app.route('/booking-list', methods = ['post', 'get'])
@login_required
def booking_list():
    if current_user.user_role == UserRole.STAFF:
    
        roomBooking = utils.load_room_booking()
        err_msg = ""
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            roomid = request.form.get('roomid')
            user = utils.get_user_by_username(user_name=username.strip())
            try:
                    return redirect(url_for('booking-list'))
            except Exception as ex:
                err_msg = 'He thong dang co loi:' + str(ex)

        return render_template('bookinglist.html', roomBooking=roomBooking)
    else:
        abort(403)
        
@app.route('/api/booking/payment', methods=['get', 'post'])
@login_required
def booking_payment():
    if current_user.user_role == UserRole.STAFF:
    
        err_msg = ''
        receipt_id = request.json.get('receipt_id')
        if receipt_id:
            if request.method.__eq__('POST'):
                in_price = request.json.get('in_price')
                total_price = request.json.get('total_price')
                if in_price and total_price and total_price <= in_price:
                    booking_pay_by_id(receipt_id)
                    return jsonify({
                        'code': 200,
                        'msg': 'Thanh toán thành công'
                    })
                else:
                    return jsonify({
                    'code': 200,
                    'price': utils.get_booking_total_price(receipt_id)
                    })

        

        else:
            err_msg = 'Không nhận được receipt_id trên server!'
            return jsonify({
                'code': 404,
                'err_msg': err_msg
            })
    else:
        abort(403)
        

@app.route('/api/booking/cancel-booking', methods=['delete'])
@login_required
def cancel_booking():
    if current_user.user_role == UserRole.STAFF:

        receipt_id = request.json.get('receipt_id')
        err_msg = ''
        if receipt_id:
                utils.room_booking_cancel(receipt_id)
                return jsonify({
                    'code': 200,
                    'data': utils.load_room_booking()
                })
    
        else:
            err_msg = 'Thông tin đặt phòng không tồn tại!'

        return jsonify({
            'code': 404,
            'err_msg': err_msg
        })
    else:
        abort(403)


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

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = 'Username or password INCORRECT'


    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))




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
@login_required
def cart():
    return render_template('cart.html',
                           cart_stats=utils.cart_stats(session.get('cart')))


@app.route('/api/add-to-cart', methods=['post'])
@login_required
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
@login_required
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
@login_required
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


@app.route("/rooms/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(room_id)
    comments = utils.get_comments(request.args.get('page', 1))

    return render_template('details.html',
                           room=room,
                           comments=comments)

@app.route("/receipts/<int:receipt_id>")
def receipt_detail(receipt_id):

    receipt = utils.get_receipt_by_receiptid(receipt_id)
    user = utils.get_user_by_id(receipt.user_id)
    receiptDetail = utils.get_receipt_detail_by_receipt_id(receipt_id)
    listDT = utils.get_list_by_receiptid(receipt_id)
    room = utils.get_room_by_id(receiptDetail.room_id)
    return render_template('ReceiptDetail.html',
                           receipt = receipt,
                           receiptDetail=receiptDetail,
                           user=user,
                           listDT=listDT,
                           room=room)

@app.route('/api/comments', methods=['post'])
@login_required
def add_comment():
    data = request.json
    content = data.get('content')
    room_id = data.get('room_id')

    try:
        c = utils.add_comment(content=content, room_id=room_id)
    except:
        return {'status': 404, 'err_msg': 'Chuong trinh dang bi loi!!'}
    return {'status': 201, 'comment': {
        'id': c.id,
        'content': c.content,
        'created_date': c.created_date,
        'user':{
            'username': current_user.username,
            'avatar' : current_user.avatar
        }
    }}


@app.context_processor
def common_response():
    return {
        'kind': utils.load_kind(),
        'userRole' : UserRole,
        'cart_stats': utils.cart_stats(session.get('cart'))
    }

if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)