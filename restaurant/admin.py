from django.contrib import admin
from .models import OpenDay, Booking

@admin.register(OpenDay)
class OpenDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_open', 'total_seats')
    list_filter = ('is_open',)
    search_fields = ('date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'open_day', 'seats_booked', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('user__username', 'open_day__date')
