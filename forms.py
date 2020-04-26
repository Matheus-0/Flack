from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo, InputRequired, Length


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
