from flask_wtf import FlaskForm
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


class LoginForm(FlaskForm):
    username = StringField('username', [
        InputRequired('Username is required.')
    ])

    password = StringField('password', [
        InputRequired('Password is required.')
    ])

    submit = SubmitField('Log In')
