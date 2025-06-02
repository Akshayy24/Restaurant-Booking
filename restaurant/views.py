from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import OpenDay, Booking
from .forms import BookingForm, OpenDayForm
from django.conf import settings

def home_view(request):
    return render(request, 'restaurant/home.html')

@login_required
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('booking_history')
    else:
        form = BookingForm(user=request.user)
    return render(request, 'restaurant/booking_form.html', {'form': form})

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'restaurant/booking_history.html', {'bookings': bookings})

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'



@user_passes_test(is_admin)
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'approved'
    booking.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status != 'cancelled':
        booking.open_day.total_seats += booking.seats_booked
        booking.open_day.save()
        booking.status = 'cancelled'
        booking.save()
    return redirect('admin_dashboard')

@user_passes_test(is_admin)
def add_open_day(request):
    if request.method == 'POST':
        form = OpenDayForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            if OpenDay.objects.filter(date=date).exists():
                form.add_error('date', 'This date is already registered as open.')
            else:
                form.save()
                return redirect('admin_dashboard')
    else:
        form = OpenDayForm()
    return render(request, 'restaurant/add_open_day.html', {'form': form})

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

@csrf_exempt
@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user, status='approved', is_paid=False)

    # Razorpay credentials
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET))

    amount = booking.seats_booked * 10000  # ₹1000 per seat -> in paise
    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

    booking.razorpay_order_id = payment['id']
    booking.save()

    return render(request, 'restaurant/payment.html', {
        'booking': booking,
        'payment': payment,
        'razorpay_key':settings.RAZORPAY_API_KEY,
        'amount': amount,
    })

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, id=booking_id)
        booking.is_paid = True
        booking.save()
        return redirect('booking_history')
    return HttpResponseBadRequest("Invalid Request")


@login_required
def admin_dashboard(request):
    return render(request, 'restaurant/admin_dashboard.html')

@user_passes_test(is_admin)
def admin_dashboard(request):
    open_days = OpenDay.objects.all().order_by('date')
    bookings = Booking.objects.select_related('user', 'open_day').all()

    if request.method == 'POST':
        form = OpenDayForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = OpenDayForm()

    return render(request, 'restaurant/admin_dashboard.html', {
        'open_days': open_days,
        'bookings': bookings,
        'form': form,
    })
