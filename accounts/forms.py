from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    # Tambahkan field quantity ke dalam form
    quantity = forms.IntegerField(min_value=1, initial=1)

    class Meta:
        model = Order
        fields = ['customer_name', 'phone_number', 'address', 'products', 'total_price', 'quantity']
