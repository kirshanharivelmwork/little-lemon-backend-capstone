# Little Lemon — Back-End Developer Capstone

Little Lemon Django web application with static HTML pages, a MySQL backend, menu endpoints, booking APIs, user registration/authentication and unit tests. See `Readme.txt` for exact reviewer endpoints.

## 1. Setup (MySQL + Pipenv)

Install Python 3.11 or 3.12 and Pipenv if needed:

```powershell
py -m pip install --user pipenv
cd LittleLemon
pipenv install
pipenv shell
python manage.py makemigrations --check --dry-run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If `pipenv shell` is not enabled in your Pipenv version, use `pipenv run python manage.py migrate` and `pipenv run python manage.py runserver`.

Open http://127.0.0.1:8000/admin/ and log in with the superuser you created. Create users and assign groups through Django admin, or use the API endpoints below.

## 2. Authentication

- Register: `POST /api/auth/users/` with `username`, `password` and optionally `email`.
- Obtain JWT tokens: `POST /api/token/` with `username` and `password`. Response includes `access` and `refresh`.
- Refresh JWT: `POST /api/token/refresh/` with `refresh`.
- Use header: `Authorization: Bearer <access-token>`.
- Djoser endpoints are mounted under `/api/auth/`.

## 3. Endpoints and grading criteria

| Criteria | Endpoint / action |
|---|---|
| Admin assigns Manager group | `POST /api/groups/manager/users` body `{"username":"name"}` (admin/staff only) |
| Admin accesses Manager group | `GET /api/groups/manager/users` with admin token/session |
| Admin adds menu items | `POST /api/menu-items/` (admin or manager) |
| Admin adds categories | `POST /api/categories/` (admin only) |
| Manager login | `POST /api/token/` |
| Manager updates item of day | `PUT /api/menu-items-of-the-day` body `{"item_id":1}` |
| Manager assigns delivery crew group | `POST /api/groups/delivery-crew/users` body `{"username":"name"}` |
| Manager assigns orders | `PATCH /api/orders/1/assign` body `{"delivery_crew":"crew_username"}` |
| Crew sees assigned orders | `GET /api/orders` |
| Crew marks delivered | `PATCH /api/orders/1` body `{"status":"delivered"}` |
| Customer registration | `POST /api/auth/users/` |
| Customer login/token | `POST /api/token/` |
| Browse categories | `GET /api/categories/` |
| Browse menu | `GET /api/menu-items/` |
| Filter by category | `GET /api/menu-items/?category=1` |
| Paginate | `GET /api/menu-items/?page=2` (10 per page) |
| Sort by price | `GET /api/menu-items/?ordering=price` or `?ordering=-price` |
| Add cart item | `POST /api/cart/menu-items` body `{"menuitem":1,"quantity":2}` |
| View cart | `GET /api/cart/menu-items` |
| Place order | `POST /api/orders` |
| View own orders | `GET /api/orders` |

Menu browsing is public. Cart and order operations require authentication. Managers can see all orders; delivery crew see only assigned orders; customers see only their own orders.

## 4. Useful API examples

Create category (admin):
```json
{"title":"Desserts","slug":"desserts"}
```

Create menu item (admin/manager):
```json
{"title":"Lemon Cake","price":"6.50","featured":false,"category_id":1}
```

Assign user to group (admin):
```json
{"username":"manager1"}
```

Create delivery crew user in admin or via Djoser registration, then have a manager add them to the Delivery crew group.

Assign order:
```json
{"delivery_crew":"delivery1"}
```

## 5. Database and credentials

The capstone uses MySQL; create a local MySQL database named `menu_db` and configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` as environment variables. The repository does not contain database passwords or a database dump.

## 6. Tests

```powershell
python manage.py test
```

## Notes
This starter implementation is intended for a local course submission, not production deployment. Before deploying publicly, replace the development secret, set `DEBUG=False`, configure allowed hosts, HTTPS, and production-grade settings.
