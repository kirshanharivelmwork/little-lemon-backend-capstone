# Little Lemon — Meta Back-End Developer Capstone

A Django and Django REST Framework restaurant backend, using MySQL by default,
with a browseable Menu API, protected Booking API, user authentication,
restaurant pages and unit tests.

## What to review

- Django project: `littlelemon`; app: `restaurant` (also a harmless `reastaurant` alias to match the rubric typo)
- Models: `restaurant/models.py` (`Menu`, `Booking`)
- REST serializers: `restaurant/serializers.py`
- REST viewsets: `restaurant/views.py` (`MenuViewSet`, `BookingViewSet`)
- Routes: `restaurant/urls.py`, `littlelemon/urls.py`
- Unit tests: `restaurant/test_models.py`, `restaurant/test_views.py`
- Landing page: `templates/index.html` and the `index` view
- MySQL database config: `littlelemon/settings.py`

**See [`Readme.txt`](Readme.txt) for every endpoint, sample requests, and reviewer setup steps.**

To run with MySQL, create a local database and set `DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST` and `DB_PORT` as appropriate. Then run `pipenv install`,
`pipenv run python manage.py migrate`, `pipenv run python manage.py test`,
and `pipenv run python manage.py runserver`.

A `.github/workflows/django-tests.yml` workflow runs checks against a GitHub
Actions MySQL service as an automated validation aid.
