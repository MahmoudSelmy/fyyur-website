from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_core import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

