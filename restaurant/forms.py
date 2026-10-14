from django import forms
from django.utils import timezone
from .models import Booking

RESERVATION_SLOTS = [
    ("10:00", "10:00 AM"), ("11:00", "11:00 AM"),
    ("12:00", "12:00 PM"), ("13:00", "1:00 PM"),
    ("14:00", "2:00 PM"), ("15:00", "3:00 PM"),
    ("16:00", "4:00 PM"), ("17:00", "5:00 PM"),
    ("18:00", "6:00 PM"), ("19:00", "7:00 PM"),
    ("20:00", "8:00 PM"), ("21:00", "9:00 PM"),
]

class BookingForm(forms.ModelForm):
    reservation_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date", "id": "reservation-date", "required": True}),
    )
    reservation_slot = forms.ChoiceField(
        choices=RESERVATION_SLOTS,
        widget=forms.Select(attrs={"id": "reservation-slot", "required": True}),
    )

    class Meta:
        model = Booking
        fields = ["first_name", "reservation_date", "reservation_slot"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Your first name", "required": True, "autocomplete": "given-name"}),
        }

    def clean_reservation_date(self):
        date = self.cleaned_data["reservation_date"]
        if date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return date

    def clean(self):
        cleaned = super().clean()
        date = cleaned.get("reservation_date")
        slot = cleaned.get("reservation_slot")
        if date and slot and Booking.objects.filter(reservation_date=date, reservation_slot=slot).exists():
            self.add_error("reservation_slot", "That time is already booked. Please choose another slot.")
        return cleaned
