from flask import Flask, render_template, request, url_for, flash
from models import db, Admin, User, ParkingLot, ParkingSpot, ReserveParkingSpot

from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html') 