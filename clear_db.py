from app import app, db
from models.models import User, ParkingLot, ParkingSpot, ReserveParkingSpot

def clear_database():
    with app.app_context():
        try:
            print("Deleting all records from ReserveParkingSpot...")
            ReserveParkingSpot.query.delete()
            print("Deleting all records from ParkingSpot...")
            ParkingSpot.query.delete()
            print("Deleting all records from ParkingLot...")
            ParkingLot.query.delete()
            print("Deleting all non-admin users from User...")
            User.query.filter_by(is_admin=False).delete()
            db.session.commit()
            print("✅ Database cleared successfully!")
            print("📊 Current database status:")
            admin_count = User.query.filter_by(is_admin=True).count()
            user_count = User.query.filter_by(is_admin=False).count()
            lot_count = ParkingLot.query.count()
            spot_count = ParkingSpot.query.count()
            booking_count = ReserveParkingSpot.query.count()
            print(f"   - Admin users: {admin_count}")
            print(f"   - Regular users: {user_count}")
            print(f"   - Parking lots: {lot_count}")
            print(f"   - Parking spots: {spot_count}")
            print(f"   - Bookings: {booking_count}")
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    clear_database() 