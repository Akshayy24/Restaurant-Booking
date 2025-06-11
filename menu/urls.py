from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_menu, name='food_menu'),
    path('order/', views.place_order, name='place_order'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
