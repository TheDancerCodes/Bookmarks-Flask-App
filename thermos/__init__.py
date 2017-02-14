"""Contains all application setup."""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Determine path to current python file
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '9\xbcl\xeb\x83s\xa5]\xf7 +5c\xbd\xafh)\xfcts\xb2Y\x1f\xbd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'birika.db')
app.config['DEBUG'] = True
# Initialise SQLAlchemy
# db variable reps DB connection & provides access to all flask_alchemy functionality
db = SQLAlchemy(app)

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

import models
import views
