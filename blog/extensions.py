from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_combo_jsonapi import Api

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
api = Api()