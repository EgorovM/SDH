from flask_pymongo import PyMongo
from flask import Flask
from pymongo import database


def get_db(app: Flask) -> database.Database:
    mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/sdh_db")
    db = mongodb_client.db

    return db
