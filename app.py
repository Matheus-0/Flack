from time import localtime, strftime

from flask import flash, Flask, redirect, render_template, url_for
from flask_login import current_user, LoginManager, login_user, logout_user
from flask_socketio import join_room, leave_room, SocketIO

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

# Rooms
rooms = ['lounge', 'news', 'games', 'coding']

# Setting up Flask's login
login = LoginManager(app)
login.init_app(app)


# Loading user by ID
@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


# Chat route
@app.route('/', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        flash('You need to log in to access this page.', 'danger')

        return redirect(url_for('login'))

    return render_template('index.html', username=current_user.username, rooms=rooms)


# Register route (change later)
@app.route('/register', methods=['GET', 'POST'])
def register():
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

    return render_template('register.html', form=registration_form)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # If method was POST
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()

        login_user(user)

        return redirect(url_for('index'))

    return render_template('login.html', form=login_form)


# Logout route
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()

    flash('You have logged out successfully.', 'success')

    return redirect(url_for('login'))


# Message event
@socket.on('message')
def message(data):
    socket.send({
        'message': data['message'],
        'username': data['username'],
        'timestamp': strftime('%b %d %I:%M%p', localtime())
    }, room=data['room'])


# Join room
@socket.on('join')
def join(data):
    join_room(data['room'])

    socket.send({
        'message': data['username'] + ' has joined the ' + data['room'] + ' room.'
    }, room=data['room'])


# Leave room
@socket.on('leave')
def leave(data):
    leave_room(data['room'])

    socket.send({
        'message': data['username'] + ' has left the ' + data['room'] + ' room.'
    }, room=data['room'])


# Run SocketIO app
if __name__ == '__main__':
    socket.run(app, debug=True)
