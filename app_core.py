from flask import Flask
from config import DEBUG, SQLALCHEMY_DATABASE_URI
from flask_moment import Moment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

moment = Moment(app)
app.config.from_object('config')