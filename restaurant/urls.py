from django.urls import path
from .views import home_view, make_booking, booking_history, admin_dashboard, approve_booking, cancel_booking, add_open_day
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', home_view, name='home'),
    path('book/', make_booking, name='make_booking'),
    path('history/', booking_history, name='booking_history'),
    path('admin_dashboard/', login_required(admin_dashboard), name='admin_dashboard'),
    path('admin_approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('admin_cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('admin_add-open-day/', add_open_day, name='add_open_day'),
]

from .views import initiate_payment, payment_success

urlpatterns += [
    path('payment/<int:booking_id>/', initiate_payment, name='initiate_payment'),
    path('payment/success/', payment_success, name='payment_success'),
]