Little Lemon Back-End Developer Capstone — reviewer guide

Project: LittleLemon (Django), app: restaurant
Database: MySQL (configure DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT).

Pages:
/
 /book/
 /reservations/

Menu API:
GET /api/categories/
GET /api/menu-items/
GET /api/menu-items/?ordering=price
POST /api/menu-items/ (admin or manager)

Table booking API (Django REST Framework):
GET  /api/bookings/
GET  /api/bookings/?date=2026-10-15
POST /api/bookings/ (authenticated)
GET  /api/bookings/<id>/
PUT  /api/bookings/<id>/ (authenticated)
PATCH /api/bookings/<id>/ (authenticated)
DELETE /api/bookings/<id>/ (authenticated)

Additional public booking endpoints:
GET /bookings
GET /bookings?date=2026-10-15
GET /available-slots/?date=2026-10-15

Authentication:
POST /api/auth/users/  (Djoser user registration)
POST /api/token/ (JWT access and refresh)
POST /api/token/refresh/
GET /api/auth/users/me/ (Bearer token required)

Setup:
python -m pip install pipenv
pipenv install
Set your local MySQL connection values as environment variables.
Create the MySQL database first, then:
pipenv run python manage.py makemigrations --check --dry-run
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
pipenv run python manage.py test
pipenv run python manage.py runserver

Sample reservation payload:
{"first_name":"Alex","reservation_date":"2026-10-15","reservation_slot":"18:00"}

This repository is for peer evaluation. Do not put real database passwords or tokens in Git.
