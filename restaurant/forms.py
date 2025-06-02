from django import forms
from .models import Booking, OpenDay
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['open_day', 'seats_booked']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['open_day'].queryset = OpenDay.objects.filter(is_open=True)
        self.instance.user = user

    def clean(self):
        cleaned_data = super().clean()
        open_day = cleaned_data.get('open_day')
        seats_booked = cleaned_data.get('seats_booked')

        if open_day and seats_booked:
            if open_day.total_seats < seats_booked:
                raise ValidationError(f"Only {open_day.total_seats} seats available.")

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        open_day = booking.open_day

        # Deduct the booked seats
        open_day.total_seats -= booking.seats_booked
        open_day.save()

        if commit:
            booking.save()
        return booking

class OpenDayForm(forms.ModelForm):
    class Meta:
        model = OpenDay
        fields = ['date', 'is_open', 'total_seats']