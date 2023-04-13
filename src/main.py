from crypt import methods
import controllers
from flask import Flask, request

from services.main_api import *
app = Flask(__name__)


@app.route('/update_predictions/<user_id>')
def update_predictions(user_id):
    print("is called")
    return controllers.update_predictions(user_id)


@app.route('/sentence_to_vec', methods=['POST'])
def sentence_to_vec():
    return controllers.sentence_to_vec(request)


if __name__ == '__main__':
    app.run()
