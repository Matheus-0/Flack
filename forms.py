from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length, ValidationError

from models import User


class RegistrationForm(FlaskForm):
    username = StringField('username', [
        InputRequired('Username required.'),
        Length(4, 32, 'Username must be between 4 and 32 characters.')
    ])

    password = PasswordField('password', [
        InputRequired('Password required.'),
        Length(4, 32, 'Password must be between 4 and 32 characters.')
    ])

    confirm = PasswordField('confirm', [
        InputRequired('Confirming password required.'),
        EqualTo('password', 'Passwords must match.')
    ])

    submit = SubmitField('Register')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username already exists.')


def invalid_credentials(form, field):
    username = form.username.data
    password = field.data

    user = User.query.filter_by(username=username).first()

    if user is None or not pbkdf2_sha256.verify(password, user.password):
        raise ValidationError("Username or password is incorrect.")


class LoginForm(FlaskForm):
    username = StringField('username', [
        InputRequired('Username is required.'),
    ])

    password = PasswordField('password', [
        InputRequired('Password is required.'),
        invalid_credentials
    ])

    submit = SubmitField('Log In')
