from django.urls import path, re_path
from . import views
from .api import BookingListCreateAPI, BookingDetailAPI

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("bookings", views.bookings_api, name="bookings-api"),
    path("bookings/", views.bookings_api),
    path("api/bookings/", BookingListCreateAPI.as_view(), name="rest-bookings"),
    re_path(r"^api/bookings/(?P<pk>[0-9]+)/$", BookingDetailAPI.as_view(), name="rest-booking-detail"),
    path("available-slots/", views.available_slots_api, name="available-slots-api"),
]
