import os

from flask import Flask

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    return 'This is the index page.'


if __name__ == '__main__':
    app.run()