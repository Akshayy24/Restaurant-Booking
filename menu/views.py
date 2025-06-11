from django.shortcuts import render, redirect
from .models import FoodItem, Order
from .forms import OrderForm

def food_menu(request):
    items = FoodItem.objects.filter(available=True)
    return render(request, 'menu/food_menu.html', {'items': items})

def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.total_price = sum(item.price for item in form.cleaned_data['food_items'])
            order.save()
            form.save_m2m()
            return redirect('order_success')
    else:
        form = OrderForm()
    return render(request, 'menu/place_order.html', {'form': form})

def order_success(request):
    return render(request, 'menu/order_success.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'menu/my_orders.html', {'orders': orders})