from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['city'].initial = user.city
            self.fields['address'].initial = user.address
            self.fields['postal_code'].initial = user.postal_code