LITTLE LEMON — META BACK-END DEVELOPER CAPSTONE

Django project directory: littlelemon
Django app: restaurant (alias `reastaurant` included because the peer rubric misspells the name)
Also includes LittleLemonAPI (additional restaurant order/menu API).

Setup on reviewer machine (Python 3.11+, MySQL running):
  python -m pip install pipenv
  pipenv install
  CREATE DATABASE menu_db CHARACTER SET utf8mb4;    (run in mysql shell)
  export DB_NAME=menu_db DB_USER=root DB_PASSWORD=YOUR_LOCAL_PASSWORD
  pipenv run python manage.py migrate
  pipenv run python manage.py createsuperuser
  pipenv run python manage.py test
  pipenv run python manage.py runserver

Open these URLs in browser / Insomnia (default http://127.0.0.1:8000):
  GET /                        Django HTML landing page (templates/index.html + restaurant/templates/index.html)
  GET /book/                   Form, date picker and available time slots
  GET /reservations/           Reservation browser
  GET /bookings?date=2026-10-17          JSON reservations for a date
  GET /available-slots/?date=2026-10-17  Availability JSON
  GET /api/menu/              DRF browsable Menu list
  GET /api/menu/1/            DRF browsable Menu detail
  POST /api/menu/             Create Menu (staff token or session)
  PUT/PATCH/DELETE /api/menu/1/   Staff only
  GET /api/bookings/          DRF browsable Booking list
  GET /api/bookings/?date=2026-10-17      DRF date filter
  POST /api/bookings/         Create Booking (authenticated)
  GET/PUT/PATCH/DELETE /api/bookings/1/   Detail and updates; writes require authentication
  POST /api-token-auth/       Django REST Framework token authentication
  POST /api/api-token-auth/   Alias for token authentication
  POST /auth/users/          Djoser user registration
  GET /auth/users/me/        Djoser authenticated user endpoint
  POST /auth/jwt/create/     Djoser JWT token login
  POST /api/token/           JWT token login
  GET /api/menu-items/       Additional menu API (LittleLemonAPI)
  GET /api/categories/       Category listing

Insomnia request examples:
  POST /api-token-auth/  JSON {"username":"YOUR_USER","password":"YOUR_PASSWORD"}
  Use header Authorization: Token YOUR_TOKEN for protected endpoints.
  POST /api/bookings/ JSON {"first_name":"Alex","reservation_date":"2026-10-17","reservation_slot":"18:00"}
  POST /api/menu/ JSON {"title":"Greek salad","price":"12.50","inventory":20} (staff)

Unit test files required by rubric: restaurant/test_models.py, restaurant/test_views.py.
For tests without MySQL service, set DB_ENGINE=sqlite in environment before running tests.
No database passwords or personal access tokens are stored in the project.

Rubric checklist (14 items):
  Project littlelemon/ and app restaurant/ (reastaurant/ compatibility alias).
  INSTALLED_APPS includes restaurant, reastaurant, rest_framework, djoser.
  TEMPLATES DIRS includes BASE_DIR / templates.
  index.html is served at / by restaurant.views.index.
  MySQL is the default DATABASES engine; set local DB environment variables.
  restaurant.models declares Menu and Booking, both registered in restaurant.admin.
  restaurant.serializers provides MenuSerializer and BookingSerializer.
  restaurant.views has MenuViewSet and BookingViewSet.
  restaurant.urls has api-token-auth/ mapped to DRF obtain_auth_token.
  littlelemon.urls includes Djoser registration, user and JWT routes.
  /api/menu/ and /api/bookings/ are DRF browsable API endpoints.
  restaurant/test_models.py and restaurant/test_views.py cover required functionality.
  Test the same API endpoints using Insomnia or another REST client.
