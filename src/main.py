import controllers
from flask import Flask, request

from services.main_api import *
app = Flask(__name__)


@app.route('/update_predictions/<user_id>')
def update_predictions(user_id):
    print("is called")
    return controllers.update_predictions(user_id)


@app.route('/sentence_to_vec/<sentence>')
def sentence_to_vec(sentence):
    return controllers.sentence_to_vec(sentence)


if __name__ == '__main__':
    app.run()
