from django.db import IntegrityError, transaction
from rest_framework import generics, permissions, serializers
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Booking.objects.all()

    def get_queryset(self):
        query = super().get_queryset()
        date = self.request.query_params.get("date")
        return query.filter(reservation_date=date) if date else query

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as exc:
            raise serializers.ValidationError("This slot is already booked.") from exc

class BookingDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as exc:
            raise serializers.ValidationError("This slot is already booked.") from exc
