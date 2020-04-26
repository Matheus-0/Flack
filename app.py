from flask import Flask, render_template

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

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return 'Success!'

    return render_template('index.html', form=registration_form)


if __name__ == '__main__':
    app.run()
