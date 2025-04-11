from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OrderPaymentItem

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrderPaymentItemForm(forms.ModelForm):
    statuses = [
        ('NEW', 'NEW'),
        ('APPROVED',"APPROVED"),
        ('REJECTED',"REJECTED")
    ]
    status = forms.ChoiceField(choices=statuses)
    class Meta:
        model = OrderPaymentItem
        fields = ['payor', 'address', 'fee_type_1', 'fee_type_1_amount', 
                  'fee_type_2', 'fee_type_2_amount', 'fee_type_3', 'fee_type_3_amount',
                  'dst', 'surcharge', 'total_amount', 'amount_in_words', 
                  'bill_no', 'bill_date', 'status', 'bank_name', 'account_number',
                  'deposit_amount']