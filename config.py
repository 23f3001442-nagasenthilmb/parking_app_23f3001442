from dotenv import load_dotenv
import os
load_dotenv()
from app import app, db
app.config('SQLACHEMY_DATABASE_URI') = os.getenv('SQLACHEMY_DATABASE_URI')

app.config('SQLALCHEMY_TRACK_MODIFICATION') = os.getenv('SQLACHEMY_DATABASE_URI')
