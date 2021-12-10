from hotelapp import app
from flask import render_template


@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)