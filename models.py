from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """user model with registration and authentication"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, form):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(form.password.data)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls()
        form.populate_obj(user)
        user.password = hashed_utf8

        # return instance of user w/username and hashed pwd
        return user

    @classmethod
    def authenticate(cls, form):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=form.username.data).first()

        if u and bcrypt.check_password_hash(u.password, form.password.data):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    """feedback model"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False,  unique=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

    user = db.relationship('User', backref=backref('feedback', cascade='all, delete-orphan'))
