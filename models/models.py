from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db

class Admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(512), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(32), primary_key=True)
    password_hash = db.Column(db.String(512), nullable=False)
    fullname = db.Column(db.String(64), nullable=False)
    phonenumber = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    pincode = db.Column(db.String(6), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    vehicle_number = db.Column(db.String(20), nullable=False)


with app.app_context():
    try:
        db.create_all()
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                fullname='Administrator',
                phonenumber='0000000000',
                address='System Address',
                pincode='000000',
                is_admin=True
            )
            admin.password = 'admin'  
            db.session.add(admin)
            admin_entry = Admin(
                username='admin',
                password=generate_password_hash('admin')
            )
            db.session.add(admin_entry)
            db.session.commit()
            print('Admin user created successfully')
        else:
            print('Admin user already exists')
    except Exception as e:
        print(f'Error during database setup: {e}')
