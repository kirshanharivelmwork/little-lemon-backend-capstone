# Little Lemon Booking Assessment

This version builds the Django booking-form assessment on top of the uploaded Little Lemon API project. The existing `LittleLemonAPI` app and its API routes are retained, and a new `restaurant` app implements the booking workflow.

## Requirements
- Python 3.11 (matches the included Pipfile)
- Pipenv
- MySQL Server

## 1. Create the database
Log in to MySQL and run:

```sql
CREATE DATABASE menu_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

In Windows PowerShell, set the credentials for your own local MySQL account. Do not share or submit a real password in screenshots:

```powershell
$env:DB_NAME = "menu_db"
$env:DB_USER = "root"
$env:DB_PASSWORD = "YOUR_LOCAL_MYSQL_PASSWORD"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
```

If your MySQL root account has no password, set `DB_PASSWORD` to an empty string.

## 2. Install and migrate
Run from the folder containing `manage.py`:

```powershell
pip install pipenv
pipenv install
pipenv run python manage.py makemigrations restaurant
pipenv run python manage.py migrate
pipenv run python manage.py test restaurant
pipenv run python manage.py runserver
```

If your environment supports `pipenv shell`, you can activate it and use `python manage.py ...` commands instead.

## 3. Pages and endpoints
- Home: `http://127.0.0.1:8000/`
- Booking form: `http://127.0.0.1:8000/book/`
- Reservations page: `http://127.0.0.1:8000/reservations/`
- All bookings as JSON: `http://127.0.0.1:8000/bookings`
- Bookings for one date: `http://127.0.0.1:8000/bookings?date=2026-10-15`
- Available time slots: `http://127.0.0.1:8000/available-slots/?date=2026-10-15`

The booking database has a unique constraint on reservation date + reservation slot, so duplicate slots are prevented even if two submissions happen close together. The JavaScript fetches available slots whenever the selected date changes.

## Important
The provided ZIP was originally a Django REST Framework API project and did not include the original Coursera website templates/assets. This submission preserves the API project and adds a simple working booking/reservations interface for the requested assessment. Review the pages locally before submission and ensure your MySQL credentials work on your computer.
