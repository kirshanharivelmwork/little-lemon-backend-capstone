"""Django REST Framework serializers for the capstone models."""
from rest_framework import serializers
from .models import Booking, Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "title", "price", "inventory"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]

    def validate(self, attrs):
        booking_date = attrs.get("reservation_date", getattr(self.instance, "reservation_date", None))
        slot = attrs.get("reservation_slot", getattr(self.instance, "reservation_slot", None))
        matches = Booking.objects.filter(reservation_date=booking_date, reservation_slot=slot)
        if self.instance is not None:
            matches = matches.exclude(pk=self.instance.pk)
        if matches.exists():
            raise serializers.ValidationError({"reservation_slot": "This date and time slot is already booked."})
        return attrs
