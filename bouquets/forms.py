from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'phone', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }