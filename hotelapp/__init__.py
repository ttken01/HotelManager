from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary

app = Flask(__name__)
app.secret_key = 'alfdsjkbgaksjfjksdgakldg21432543@#$@#'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:230801@localhost/hotelapp?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8

db = SQLAlchemy(app = app)

cloudinary.config(
            cloud_name='dn9h5wifn' ,
            api_key='146516347122523',
            api_secret='OjC1JTP9H0TLft99LmGp78VXl7w',
)
