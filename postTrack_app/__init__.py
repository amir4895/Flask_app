import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from flask_moment import Moment
app_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xb3\x15\xea\x94\xb0\xdd{\xb3\x9aC \x1d\xb7\xe1\x88\r\xde#k\x88\xd1\xdfS|'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app_dir, 'postTrack_app.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection  = 'strong'
login_manager.login_view = "login"
login_manager.init_app(app)


moment = Moment(app)

import postTrack_app.models
import postTrack_app.views
