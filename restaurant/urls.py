"""Routes for the HTML site, table bookings, and DRF viewsets."""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

menu_collection = views.MenuViewSet.as_view({"get": "list", "post": "create"})
menu_detail = views.MenuViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})
booking_collection = views.BookingViewSet.as_view({"get": "list", "post": "create"})
booking_detail = views.BookingViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})

urlpatterns = [
    path("", views.index, name="home"),
    path("book/", views.book, name="book"),
    path("reservations/", views.reservations, name="reservations"),
    path("bookings", views.bookings_api, name="bookings-api"),
    path("bookings/", views.bookings_api),
    path("available-slots/", views.available_slots_api, name="available-slots-api"),
    path("api/menu/", menu_collection, name="restaurant-menu-list"),
    path("api/menu/<int:pk>/", menu_detail, name="restaurant-menu-detail"),
    path("api/bookings/", booking_collection, name="rest-bookings"),
    path("api/bookings/<int:pk>/", booking_detail, name="rest-booking-detail"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
