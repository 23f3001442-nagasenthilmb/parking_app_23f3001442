from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(512), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(64), nullable=False)
    phonenumber = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)

class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    lot_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False) 
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    spot_id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.lot_id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')

class ReserveParkingSpot(db.Model): 
    __tablename__ = 'reserve_parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.spot_id'), nullable=False)
    user_id = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=False)
    parking_cost = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()
