from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import mixins,LoginManager
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)
# csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from app import routes,models