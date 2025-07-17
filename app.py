from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

import config

class Admin(db.Model):
    __tablename__='admin'
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(512), nullable=False)

class User(db.Model):
    __tablename__='user'
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(64), nullable=False)
    phonenumber = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)

class ParkingLot(db.Model):
    __tablename__='parking_lot'
    lot_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200), nullable=False)
    price = db.column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    spots = db.relationship('ParkingSpot', backref='lot', lazy=True)

class ParkingSpot(db.Model):
    __tablename__='parking_spot'
    spot_id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')
