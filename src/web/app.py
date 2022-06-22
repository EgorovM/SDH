from flask import Flask
from flask import request, jsonify
from flask import render_template

from web.db import get_db
from web.crud import get_user_session_by_id, insert_user_session


app = Flask(__name__)
db = get_db(app)


@app.route("/")
def hello_world():
    return render_template("index.html", name='world')


@app.route("/bot/", methods=["POST"])
def bot():
    params = request.get_json()
    message = params.get('message', '')
    action = params.get('action', None)

    user_id = 1  # todo: from params
    user_session = get_user_session_by_id(db, user_id)
    
    if not action:
        response = user_session.get_response(message)
    else:
        response = user_session.process_action(action)

    insert_user_session(db, user_session)

    return {'message': response}
