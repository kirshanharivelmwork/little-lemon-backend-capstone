"""Tests of the two models required by the Meta capstone."""
from datetime import timedelta
from decimal import Decimal
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone
from .models import Menu, Booking

class ModelTests(TestCase):
    def test_menu_model(self):
        menu = Menu.objects.create(title="Greek salad", price=Decimal("12.50"), inventory=8)
        self.assertEqual(str(menu), "Greek salad")
        self.assertEqual(menu.price, Decimal("12.50"))
        self.assertEqual(Menu.objects.count(), 1)

    def test_booking_model(self):
        day = timezone.localdate() + timedelta(days=1)
        booking = Booking.objects.create(first_name="Alex", reservation_date=day, reservation_slot="18:00")
        self.assertEqual(booking.first_name, "Alex")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Booking.objects.create(first_name="Jamie", reservation_date=day, reservation_slot="18:00")
