from django.urls import path
from . import views
from .api import BookingListCreateAPI, BookingDetailAPI

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("bookings", views.bookings_api, name="bookings-api"),
    path("bookings/", views.bookings_api),
    path("api/bookings/", BookingListCreateAPI.as_view(), name="rest-bookings"),
    path("available-slots/", views.available_slots_api, name="available-slots-api"),
]
