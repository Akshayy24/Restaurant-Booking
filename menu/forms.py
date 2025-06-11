from django import forms
from .models import Order, FoodItem

class OrderForm(forms.ModelForm):
    food_items = forms.ModelMultipleChoiceField(
        queryset=FoodItem.objects.filter(available=True),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Order
        fields = ['food_items']
