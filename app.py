from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
<<<<<<< HEAD
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

from controllers.routes import *
from models.models import *
=======
app.secret_key = 'your_secret_key'  # Set a strong secret key for session management

db = SQLAlchemy(app)

from models.models import *

from controllers.routes import *
>>>>>>> 30c5d1bfd89f8e11235a36f8bd9486322fbae987
