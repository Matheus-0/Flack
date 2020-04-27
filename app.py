from flask import flash, Flask, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_socketio import SocketIO

from forms import *
from models import *

# Setting up app
app = Flask(__name__)

app.secret_key = 'dev'

# Setting up database
app.config['SQLALCHEMY_DATABASE_URI'] = None

db = SQLAlchemy(app)

# Setting up Flask's SocketIO
socket = SocketIO(app)

# Setting up Flask's login
login = LoginManager(app)
login.init_app(app)


# Loading user by ID
@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


# Register route (change later)
@app.route('/', methods=['GET', 'POST'])
def index():
    registration_form = RegistrationForm()

    # If method was POST
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(username, hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Signed up successfully. You can log in now.', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=registration_form)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # If method was POST
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        login_user(user)

        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)


# Chat route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('You need to log in to access this page.', 'danger')

        return redirect(url_for('login'))

    return render_template('chat.html')


# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()

    flash('You have logged out successfully.', 'success')

    return redirect(url_for('login'))


# Message event
@socket.on('message')
def message(data):
    socket.send(data)


# Run SocketIO app
if __name__ == '__main__':
    socket.run(app, debug=True)
