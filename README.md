# Parking App

A simple parking lot management web application built with Flask and SQLite.

## Features
- User registration and login
- Admin and user dashboards
- Book and release parking spots
- View parking lot statistics and summaries
- Responsive Bootstrap UI

## Requirements
- Python 3.8+
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/23f3001442-nagasenthilmb/parking_app_23f3001442.git
   cd parking_app_23f3001442
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   The database will be created automatically on first run. If you want to clear or reset the database, use:
   ```sh
   python clear_db.py
   ```

5. **Run the application:**
   ```sh
   python app.py
   ```
   The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Default Admin Login
- Username: admin
- Password: admin

## Notes
- For development only. Do not use the default admin credentials in production.
- The database file is stored in `instance/db.sqlite3`.

## License
This project is for educational/demo purposes. 