from django.db import models
from django.conf import settings

class OpenDay(models.Model):
    date = models.DateField(unique=True)
    is_open = models.BooleanField(default=True)
    total_seats = models.IntegerField(default=0)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')

class Booking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('cancelled', 'Cancelled')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    open_day = models.ForeignKey(OpenDay, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)