from flask import Flask, redirect, render_template, url_for
from passlib.hash import pbkdf2_sha256

from forms import *
from models import *

app = Flask(__name__)

app.secret_key = 'dev'

app.config['SQLALCHEMY_DATABASE_URI'] = None

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('index.html', form=registration_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        return 'Logged in!'

    return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run()
