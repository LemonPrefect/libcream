import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *

from . import config

app = Flask(__name__, static_url_path="")
CORS(app, supports_credentials=True)
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)
database = SQLAlchemy(app)

from app import models, views
