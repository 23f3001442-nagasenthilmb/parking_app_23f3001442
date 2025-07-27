from flask import Flask, render_template, request, url_for, flash, redirect, session
from models import db, Admin, User, ParkingLot, ParkingSpot, ReserveParkingSpot
from functools import wraps
from datetime import datetime, timedelta

from app import app

def authenticate(func):
    @wraps(func)
    def inner_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please login to continue!")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner_function

@app.route('/')
@authenticate
def index():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:   
            lots = ParkingLot.query.all()
            for lot in lots:
                lot.available_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='A').count()
                lot.occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='O').count()
            
            location_filter = request.args.get('location', '')
            price_range = request.args.get('price_range', '')
            
            if location_filter:
                lots = [lot for lot in lots if location_filter.lower() in lot.location.lower() or location_filter.lower() in lot.address.lower()]
            
            if price_range:
                if price_range == '0-50':
                    lots = [lot for lot in lots if lot.price <= 50]
                elif price_range == '51-100':
                    lots = [lot for lot in lots if 51 <= lot.price <= 100]
                elif price_range == '101+':
                    lots = [lot for lot in lots if lot.price >= 101]
            
            user_bookings = ReserveParkingSpot.query.filter_by(user_id=session['user']).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
            
            for booking in user_bookings:
                spot = ParkingSpot.query.get(booking.spot_id)
                if spot:
                    booking.parking_lot = ParkingLot.query.get(spot.lot_id)
            
            total_bookings = len(user_bookings)
            active_bookings = sum(1 for booking in user_bookings if booking.leaving_timestamp > datetime.now())
            total_spent = sum(booking.parking_cost for booking in user_bookings)
            
            user_stats = {
                'total_bookings': total_bookings,
                'active_bookings': active_bookings,
                'total_spent': total_spent
            }
            
            return render_template('index.html', user=user, parking_lots=lots, user_stats=user_stats, user_bookings=user_bookings, now=datetime.now())
    else:
        flash("Please login to continue!")
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password') 
    if username == 'admin' and password == 'admin':
        user = User.query.filter_by(username='admin', is_admin=True).first()
        if user:
            session['user'] = user.username
            session['is_admin'] = True
            flash('Admin login successful!')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Admin account not found!')
            return redirect(url_for('login'))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User does not exist!')
        return redirect(url_for('login'))
    if user.is_admin:
        if password == 'admin':
            session['user'] = user.username
            session['is_admin'] = True
            flash('Admin login successful!')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect admin password!')
            return redirect(url_for('login'))
    if not user.check_password(password):
        flash('Incorrect password!')
        return redirect(url_for('login'))
    session['user'] = user.username
    session['is_admin'] = False
    flash('Login successful!')
    return redirect(url_for('index'))

@app.route('/register')
def register():
    return render_template('register.html') 

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    phonenumber = request.form.get('phonenumber')
    address = request.form.get('address')
    pincode = request.form.get('pincode')
    if User.query.filter_by(username=username).first():
        flash('Username with this username already exists!')
        return redirect(url_for('register'))
    new_user = User(
        username=username,
        password=password,
        fullname=fullname,
        phonenumber=phonenumber,
        address=address,
        pincode=pincode
    )
    db.session.add(new_user)
    db.session.commit()
    flash('Registration successful! Please login.')
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    lots = ParkingLot.query.all()
    users = User.query.filter_by(is_admin=False).all()
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    return render_template('admin_dashboard.html', lots=lots, users=users, available_spots=available_spots, occupied_spots=occupied_spots)

@app.route('/parking_lots')
def parking_lots():
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    lots = ParkingLot.query.all()
    for lot in lots:
        lot.available_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='A').count()
        lot.occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='O').count()
    return render_template('parking_lots.html', parking_lots=lots)

@app.route('/add_parking_lot', methods=['GET', 'POST'])
def add_parking_lot():
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    if request.method == 'POST':
        location = request.form.get('location')
        price = request.form.get('price')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        capacity = int(request.form.get('capacity'))
        new_lot = ParkingLot(
            location=location, 
            price=price, 
            address=address, 
            pincode=pincode, 
            capacity=capacity
        )
        db.session.add(new_lot)
        db.session.commit()
        for i in range(capacity):
            spot = ParkingSpot(
                lot_id=new_lot.lot_id
            )
            db.session.add(spot)
        db.session.commit()
        flash('Parking lot added successfully!')
        return redirect(url_for('parking_lots'))
    return render_template('add_parking_lot.html')

@app.route('/edit_parking_lot/<int:lot_id>', methods=['GET', 'POST'])
def edit_parking_lot(lot_id):
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    lot = ParkingLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.location = request.form.get('location')
        lot.price = request.form.get('price')
        lot.address = request.form.get('address')
        lot.pincode = request.form.get('pincode')
        new_capacity = int(request.form.get('capacity'))
        if new_capacity > lot.capacity:
            for i in range(lot.capacity, new_capacity):
                spot = ParkingSpot(lot_id=lot.lot_id)
                db.session.add(spot)
        elif new_capacity < lot.capacity:
            spots_to_remove = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='A').limit(lot.capacity - new_capacity).all()
            if len(spots_to_remove) < (lot.capacity - new_capacity):
                flash('Cannot reduce capacity: not enough available spots!')
                return redirect(url_for('edit_parking_lot', lot_id=lot.lot_id))
            for spot in spots_to_remove:
                db.session.delete(spot)
        lot.capacity = new_capacity
        db.session.commit()
        flash('Parking lot updated successfully!')
        return redirect(url_for('parking_lots'))
    return render_template('edit_parking_lot.html', lot=lot)

@app.route('/delete_parking_lot/<int:lot_id>', methods=['POST', 'GET'])
def delete_parking_lot(lot_id):
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    lot = ParkingLot.query.get_or_404(lot_id)
    occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id, status='O').count()
    if occupied_spots > 0:
        flash('Cannot delete lot: some spots are still occupied!')
        return redirect(url_for('parking_lots'))
    ParkingSpot.query.filter_by(lot_id=lot.lot_id).delete()
    db.session.delete(lot)
    db.session.commit()
    flash('Parking lot deleted successfully!')
    return redirect(url_for('parking_lots'))

@app.route('/view_lot_spots/<int:lot_id>')
def view_lot_spots(lot_id):
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.lot_id).all()
    
    for spot in spots:
        if spot.status == 'O':
            booking = ReserveParkingSpot.query.filter_by(spot_id=spot.spot_id).filter(
                ReserveParkingSpot.leaving_timestamp > datetime.now()
            ).first()
            if booking:
                spot.current_booking = booking
                spot.user = User.query.get(booking.user_id)
            else:
                spot.current_booking = None
                spot.user = None
    
    return render_template('view_lot_spots.html', lot=lot, spots=spots)

@app.route('/view_users')
def view_users():
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    users = User.query.filter_by(is_admin=False).all()
    return render_template('view_users.html', users=users)

@app.route('/search')
def search():
    if 'user' not in session or not session.get('is_admin'):
        flash('Admin access required!')
        return redirect(url_for('login'))
    
    search_type = request.args.get('type', 'lots')
    query = request.args.get('q', '')
    
    results = {}
    
    if search_type == 'lots':
        if query:
            results['lots'] = ParkingLot.query.filter(
                (ParkingLot.location.ilike(f'%{query}%')) |
                (ParkingLot.address.ilike(f'%{query}%')) |
                (ParkingLot.pincode.ilike(f'%{query}%'))
            ).all()
        else:
            results['lots'] = ParkingLot.query.all()
    
    elif search_type == 'users':
        if query:
            results['users'] = User.query.filter(
                (User.username.ilike(f'%{query}%')) |
                (User.fullname.ilike(f'%{query}%')) |
                (User.phonenumber.ilike(f'%{query}%')) |
                (User.address.ilike(f'%{query}%'))
            ).filter_by(is_admin=False).all()
        else:
            results['users'] = User.query.filter_by(is_admin=False).all()
    
    return render_template('search.html', search_type=search_type, query=query, results=results)

@app.route('/book_parking/<int:lot_id>', methods=['GET', 'POST'])
def book_parking(lot_id):
    if 'user' not in session:
        flash('Please login to continue!')
        return redirect(url_for('login'))
    
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    
    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number')
        
        available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        
        parking_time_str = request.form.get('parking_time')
        parking_timestamp = datetime.strptime(parking_time_str, '%Y-%m-%dT%H:%M')
        current_time = datetime.now()
        
        # Check if parking time is in the past
        if parking_timestamp < current_time:
            flash('Cannot book parking for a time in the past! Please select a future time.')
            return render_template('book_parking.html', lot=lot, spot_id=available_spot.spot_id, now=datetime.now())
        
        duration_hours = int(request.form.get('duration', 1))
        leaving_timestamp = parking_timestamp + timedelta(hours=duration_hours)
        
        base_price = lot.price
        total_cost = base_price * duration_hours
        
        reserve_spot = ReserveParkingSpot(
            spot_id=available_spot.spot_id,
            user_id=session['user'],
            parking_timestamp=parking_timestamp, 
            leaving_timestamp=leaving_timestamp,
            parking_cost=total_cost,
            vehicle_number=vehicle_number
        )
        
        available_spot.status = 'O'

        user_bookings = ReserveParkingSpot.query.filter_by(user_id=session['user']).order_by(ReserveParkingSpot.parking_timestamp.desc()).all()
        
        db.session.add(reserve_spot)
        db.session.commit()
        flash('Parking spot booked successfully!')
        return redirect(url_for('index'))
    
    return render_template('book_parking.html', lot=lot, spot_id=available_spot.spot_id, now=datetime.now())

@app.route('/release_spot/<int:booking_id>', methods=['POST'])
@authenticate
def release_spot(booking_id):
    if 'user' not in session:
        flash('Please login to continue!')
        return redirect(url_for('login'))

    booking = ReserveParkingSpot.query.get_or_404(booking_id)
    
    if booking.user_id != session['user']:
        flash('You can only release your own parking spots!')
        return redirect(url_for('index'))
    
    if booking.leaving_timestamp <= datetime.now():
        flash('This booking has already expired!')
        return redirect(url_for('index'))

    spot = ParkingSpot.query.get(booking.spot_id)
    if not spot:
        flash('Parking spot not found!')
        return redirect(url_for('index'))

    spot.status = 'A'
    
    booking.leaving_timestamp = datetime.now()
    
    actual_duration = (booking.leaving_timestamp - booking.parking_timestamp).total_seconds() / 3600
    
    if actual_duration <= 0:
        booking.parking_cost = 0
        flash('No parking fee charged - booking was not used.')
        db.session.commit()
        return redirect(url_for('index'))
    
    parking_lot = ParkingLot.query.get(spot.lot_id)
    if parking_lot:
        booking.parking_cost = int(parking_lot.price * actual_duration)
    
    db.session.commit()
    flash('Parking spot released successfully! Cost adjusted for actual duration.')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        flash('Please login to continue!')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        flash('Please login to continue!')
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['user']).first()
    if request.method == 'POST':
        user.fullname = request.form.get('name')
        user.phonenumber = request.form.get('phone')
        user.address = request.form.get('address')
        user.pincode = request.form.get('pincode')
        db.session.commit()
        flash('Profile updated successfully!')  
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('login'))