from hotelapp import app, db, login
from flask import render_template, request, redirect
import utils
from flask_login import login_user
from hotelapp.admin import *

@app.route('/')
def home():


    rooms = utils.load_room()


    return render_template('index.html', rooms = rooms)


@app.context_processor
def common_response():
    return {
        'kind' : utils.load_kind()
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


if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)