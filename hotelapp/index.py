from hotelapp import app, db
from flask import render_template
import utils


@app.route('/')
def home():


    rooms = utils.load_room()


    return render_template('index.html', rooms = rooms)


@app.context_processor
def common_response():
    return {
        'kind' : utils.load_kind()
    }


if __name__ == '__main__':
    from hotelapp.admin import *

    app.run(debug=True)