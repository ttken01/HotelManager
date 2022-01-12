from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = 'alfdsjkbgaksjfjksdgakldg21432543@#$@#'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:230801@localhost/hotelapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8
app.config['COMMENT_SIZE'] = 5


db = SQLAlchemy(app = app)

login = LoginManager(app=app)

babel = Babel(app)

#Dia phuong hoa
@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'vi'


cloudinary.config(
            cloud_name='dn9h5wifn' ,
            api_key='146516347122523',
            api_secret='OjC1JTP9H0TLft99LmGp78VXl7w',
)
