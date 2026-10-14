from datetime import date
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET
from .forms import BookingForm, RESERVATION_SLOTS
from .models import Booking

def home(request):
    return render(request, "restaurant/home.html")

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
    qs = Booking.objects.all()
    if chosen_date:
        try:
            date.fromisoformat(chosen_date)
        except ValueError:
            return JsonResponse({"error": "Use YYYY-MM-DD."}, status=400)
        qs = qs.filter(reservation_date=chosen_date)
    data = [{"id": b.pk, "first_name": b.first_name,
             "reservation_date": b.reservation_date.isoformat(),
             "reservation_slot": b.reservation_slot} for b in qs]
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
