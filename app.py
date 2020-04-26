from flask import Flask, render_template

from forms import *

app = Flask(__name__)

app.secret_key = 'dev'


@app.route('/', methods=['GET', 'POST'])
def index():
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        return "Success!"

    return render_template('index.html', form=registration_form)


if __name__ == '__main__':
    app.run()
