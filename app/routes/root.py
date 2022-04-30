from flask import Blueprint
from app import app
from app.helper import data

root = Blueprint("/", __name__)


@root.route("/", methods=["GET"])
def root1():
    return app.send_static_file("index.html")

