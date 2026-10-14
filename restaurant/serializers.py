from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]

    def validate(self, attrs):
        from django.db.models import Q
        date = attrs.get("reservation_date", getattr(self.instance, "reservation_date", None))
        slot = attrs.get("reservation_slot", getattr(self.instance, "reservation_slot", None))
        duplicates = Booking.objects.filter(reservation_date=date, reservation_slot=slot)
        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise serializers.ValidationError("This date and time slot is already booked.")
        return attrs
