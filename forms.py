from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import validators
from wtforms.validators import InputRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """Form to register new user"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """For for user to log in"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form to add or update feedback"""
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])