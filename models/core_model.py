from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_core import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)