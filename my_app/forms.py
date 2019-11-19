from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, EqualTo, Regexp, Length, Email, ValidationError
from my_app.models import User


class BookmarkForm(FlaskForm):
    url = URLField('The URL for your bookmark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        if not self.url.data:
            return False
        if self.url.data.startswith("http://") or\
            self.url.data.startswith("https://"):

            return True
        else:
            self.url.errors = ("not starting with http://",)
            return False


class ItemForm(FlaskForm):
    tracking = StringField('The tracking id for your bookmark:')
    description = StringField('Add an optional description:')

    def validate(self):
        if self.tracking.data:
            return True


class LoginForm(FlaskForm):
    username = StringField("Yore username", validators=[DataRequired()])
    password = PasswordField("Yore password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me?")
    submit = SubmitField("Log in")


class SignupForm(FlaskForm):
    username = StringField('Username',
                    validators=[
                        DataRequired(), Length(3, 80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Usernames consist of numbers, letters,'
                                    'and underscores.')])
    password = PasswordField('Password',
                    validators=[
                        DataRequired(),
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
