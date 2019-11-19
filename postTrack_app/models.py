from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from enum import Enum
from werkzeug.security import check_password_hash, generate_password_hash
from postTrack_app import db



class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        ans = URL.query.order_by(desc(URL.id)).limit(num)
        return ans

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.description, self.url)


class ItemStatus(Enum):
    open = "open"
    in_progress = "in progress"
    closed = "closed"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(300))
    status = db.Column(db.Enum(ItemStatus), default=ItemStatus.open)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        ans = Item.query.order_by(desc(Item.id)).limit(num)
        return ans

    def __repr__(self):
        return f"Track id:'{self.tracking_id}"




class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    # nick_name = db.Column(ydb.String(80), unique=False)
    # last_name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    items = db.relationship('Item', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    @staticmethod
    def newest(num):
        ans = User.query.order_by(desc(User.id)).limit(num)
        return ans
