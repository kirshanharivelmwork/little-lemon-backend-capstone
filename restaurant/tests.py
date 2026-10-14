from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Booking

class BookingAssessmentTests(TestCase):
    def setUp(self):
        self.tomorrow = timezone.localdate() + timedelta(days=1)

    def test_booking_page_loads_with_today_as_default(self):
        response = self.client.get(reverse("book"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="date"')

    def test_booking_can_be_created(self):
        response = self.client.post(reverse("book"), {
            "first_name": "Asha",
            "reservation_date": self.tomorrow.isoformat(),
            "reservation_slot": "18:00",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(
            first_name="Asha", reservation_date=self.tomorrow, reservation_slot="18:00"
        ).exists())

    def test_duplicate_date_and_slot_is_rejected(self):
        Booking.objects.create(first_name="Asha", reservation_date=self.tomorrow, reservation_slot="18:00")
        response = self.client.post(reverse("book"), {
            "first_name": "Riya",
            "reservation_date": self.tomorrow.isoformat(),
            "reservation_slot": "18:00",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.filter(reservation_date=self.tomorrow, reservation_slot="18:00").count(), 1)

    def test_bookings_api_filters_by_date(self):
        Booking.objects.create(first_name="Asha", reservation_date=self.tomorrow, reservation_slot="18:00")
        response = self.client.get(reverse("bookings-api"), {"date": self.tomorrow.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_empty_date_returns_empty_json_array(self):
        response = self.client.get(reverse("bookings-api"), {"date": self.tomorrow.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
