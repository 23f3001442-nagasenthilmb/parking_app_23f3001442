from app import app, db
<<<<<<< HEAD
from models.models import User, ParkingLot, ParkingSpot, ReserveParkingSpot
=======
from models import User, ParkingLot, ParkingSpot, ReserveParkingSpot
>>>>>>> 30c5d1bfd89f8e11235a36f8bd9486322fbae987

def clear_database():
    with app.app_context():
        try:
<<<<<<< HEAD
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
=======
            # Delete all records from each table
            print("Deleting all records from ReserveParkingSpot...")
            ReserveParkingSpot.query.delete()
            
            print("Deleting all records from ParkingSpot...")
            ParkingSpot.query.delete()
            
            print("Deleting all records from ParkingLot...")
            ParkingLot.query.delete()
            
            print("Deleting all non-admin users from User...")
            # Keep admin user, delete only regular users
            User.query.filter_by(is_admin=False).delete()
            
            # Commit the changes
            db.session.commit()
            
            print("✅ Database cleared successfully!")
            print("📊 Current database status:")
            
            # Show current counts
>>>>>>> 30c5d1bfd89f8e11235a36f8bd9486322fbae987
            admin_count = User.query.filter_by(is_admin=True).count()
            user_count = User.query.filter_by(is_admin=False).count()
            lot_count = ParkingLot.query.count()
            spot_count = ParkingSpot.query.count()
            booking_count = ReserveParkingSpot.query.count()
<<<<<<< HEAD
=======
            
>>>>>>> 30c5d1bfd89f8e11235a36f8bd9486322fbae987
            print(f"   - Admin users: {admin_count}")
            print(f"   - Regular users: {user_count}")
            print(f"   - Parking lots: {lot_count}")
            print(f"   - Parking spots: {spot_count}")
            print(f"   - Bookings: {booking_count}")
<<<<<<< HEAD
=======
            
>>>>>>> 30c5d1bfd89f8e11235a36f8bd9486322fbae987
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    clear_database() 