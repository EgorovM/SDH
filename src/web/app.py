from flask import Flask
from flask import request, jsonify
from flask import render_template

from web.db import get_db
from web.crud import get_user_session_by_id, insert_user_session
from web.settings import LOCALES


app = Flask(__name__)
db = get_db(app)


@app.route("/<string:language>")
def hello_world(language):
    language = language.lower()
    language = language or "ru"

    return render_template("index.html", **LOCALES.get(language, LOCALES["ru"]))


def get_user_id(request):
    return request.remote_addr


@app.route("/bot/", methods=["POST"])
def bot():
    params = request.get_json()
    message = params.get("message", "")
    action = params.get("action", None)
    language = params.get("language", "ru")

    user_id = get_user_id(request)
    user_session = get_user_session_by_id(db, user_id)

    if not action:
        response = user_session.get_response(message, language=language)
    else:
        response = user_session.process_action(message, action, language=language)

    insert_user_session(db, user_session)

    return {"message": response}


@app.route("/messages/", methods=["GET"])
def message():
    user_id = get_user_id(request)
    user_session = get_user_session_by_id(db, user_id)

    return {"user_session": user_session.serialize()}
