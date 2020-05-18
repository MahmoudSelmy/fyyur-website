from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_core import app
from sqlalchemy import func

db = SQLAlchemy(app)
migrate = Migrate(app, db)