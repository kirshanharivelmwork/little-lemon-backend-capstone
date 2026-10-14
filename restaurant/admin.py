from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("first_name", "reservation_date", "reservation_slot")
    list_filter = ("reservation_date",)
    search_fields = ("first_name",)
    ordering = ("reservation_date", "reservation_slot")
