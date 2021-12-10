from hotelapp import app
from flask_admin import Admin


admin = Admin(app=app, name="Hotel Website Administration", template_mode="bootstrap4")