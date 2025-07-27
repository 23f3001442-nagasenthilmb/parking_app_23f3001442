from app import app, db
from models.models import User
from datetime import datetime

def init_database():
    with app.app_context():
        try:
            # Create tables if they don't exist
            db.create_all()
            
            # Check if admin user exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # Create admin user
                admin = User(
                    username='admin',
                    password='admin',
                    fullname='Administrator',
                    phonenumber='0000000000',
                    address='System Address',
                    pincode='000000',
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print('Admin user created successfully')
            else:
                print('Admin user already exists')
                
        except Exception as e:
            print(f'Error during database setup: {e}')

if __name__ == '__main__':
    init_database() 