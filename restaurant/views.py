"""Restaurant pages and browsable Django REST Framework CRUD APIs."""
from datetime import date

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET
from rest_framework import permissions, serializers, viewsets
from rest_framework.exceptions import ValidationError

from .forms import BookingForm, RESERVATION_SLOTS
from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer

def index(request):
    """Serve the landing page using Django templates and static assets."""
    return render(request, "index.html")

def home(request):
    """Legacy homepage alias."""
    return index(request)

def book(request):
    form = BookingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
            return redirect("reservations")
        except IntegrityError:
            form.add_error("reservation_slot", "That time was just booked.")
    return render(request, "restaurant/book.html", {
        "form": form, "today": timezone.localdate().isoformat(), "slots": RESERVATION_SLOTS,
    })

def reservations(request):
    return render(request, "restaurant/reservations.html", {"today": timezone.localdate().isoformat()})

@require_GET
def bookings_api(request):
    chosen_date = request.GET.get("date")
    bookings = Booking.objects.all()
    if chosen_date:
        try:
            date.fromisoformat(chosen_date)
        except ValueError:
            return JsonResponse({"error": "Use YYYY-MM-DD."}, status=400)
        bookings = bookings.filter(reservation_date=chosen_date)
    data = [{"id": b.pk, "first_name": b.first_name,
             "reservation_date": b.reservation_date.isoformat(),
             "reservation_slot": b.reservation_slot} for b in bookings]
    return JsonResponse(data, safe=False)

@require_GET
def available_slots_api(request):
    chosen_date = request.GET.get("date")
    try:
        d = date.fromisoformat(chosen_date or "")
    except ValueError:
        return JsonResponse({"error": "Use YYYY-MM-DD."}, status=400)
    booked = set(Booking.objects.filter(reservation_date=d).values_list("reservation_slot", flat=True))
    return JsonResponse({"date": d.isoformat(), "slots": [
        {"value": value, "label": label, "available": value not in booked}
        for value, label in RESERVATION_SLOTS
    ]})

class IsStaffOrReadOnly(permissions.BasePermission):
    """Everyone can browse menu data; only Django staff can change it."""
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )

class MenuViewSet(viewsets.ModelViewSet):
    """List, create, retrieve, update and delete Menu objects."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsStaffOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    """Browse, create, retrieve, update and delete table bookings."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        date_param = self.request.query_params.get("date")
        if not date_param:
            return qs
        try:
            date.fromisoformat(date_param)
        except ValueError as exc:
            raise ValidationError({"date": "Use YYYY-MM-DD."}) from exc
        return qs.filter(reservation_date=date_param)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as exc:
            raise serializers.ValidationError({"reservation_slot": "This slot is already booked."}) from exc

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except IntegrityError as exc:
            raise serializers.ValidationError({"reservation_slot": "This slot is already booked."}) from exc
