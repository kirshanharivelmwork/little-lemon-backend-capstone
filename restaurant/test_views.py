"""Browsable REST API and HTML page tests for the Little Lemon capstone."""
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Menu, Booking

class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.today = timezone.localdate()
        cls.tomorrow = cls.today + timedelta(days=1)
        cls.user = get_user_model().objects.create_user(username="tester", password="A-test-password-92")
        cls.staff = get_user_model().objects.create_user(username="staff", password="A-test-password-92", is_staff=True)
        cls.menu = Menu.objects.create(title="Lemon soup", price=Decimal("6.00"), inventory=7)

    def test_home_serves_index_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_menu_viewset_is_browsable(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Lemon soup")

    def test_menu_create_requires_staff(self):
        api = APIClient()
        self.assertIn(api.post("/api/menu/", {"title": "Mint tea", "price": "3.50", "inventory": 5}).status_code, (401,403))
        api.force_authenticate(user=self.staff)
        response = api.post("/api/menu/", {"title": "Mint tea", "price": "3.50", "inventory": 5})
        self.assertEqual(response.status_code, 201)

    def test_bookings_list_and_create(self):
        api = APIClient()
        self.assertEqual(api.get("/api/bookings/").status_code, 200)
        api.force_authenticate(user=self.user)
        payload={"first_name": "Alex", "reservation_date": self.tomorrow.isoformat(), "reservation_slot":"18:00"}
        response=api.post("/api/bookings/", payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(api.post("/api/bookings/", payload).status_code, 400)
        self.assertEqual(Booking.objects.count(), 1)

    def test_bookings_date_filter(self):
        Booking.objects.create(first_name="Alex", reservation_date=self.tomorrow, reservation_slot="18:00")
        response = self.client.get("/api/bookings/", {"date": self.tomorrow.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(self.client.get("/api/bookings/", {"date":"invalid"}).status_code, 400)

    def test_token_authentication_endpoint(self):
        api = APIClient()
        response=api.post("/api-token-auth/", {"username": "tester", "password": "A-test-password-92"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_djoser_registration_route(self):
        from django.urls import resolve
        self.assertIsNotNone(resolve("/auth/users/"))

    def test_booking_update_and_delete(self):
        from rest_framework.test import APIClient
        api = APIClient()
        api.force_authenticate(user=self.user)
        booking = Booking.objects.create(
            first_name="Zoe", reservation_date=self.tomorrow, reservation_slot="18:00"
        )
        response = api.patch(f"/api/bookings/{booking.pk}/", {"first_name": "Zoey"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Zoey")
        response = api.delete(f"/api/bookings/{booking.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Booking.objects.filter(pk=booking.pk).exists())
