from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import OrderPaymentItem
from datetime import datetime

def generate_serial():
    year = datetime.now().year
    month = datetime.now().month
    monthly_count = OrderPaymentItem.objects.filter(
        date__year=year,
        date__month=month
    )

    if(monthly_count.count() > 0):
        last_item = monthly_count.latest('date')
        last_number = int(last_item.serial_number.split('-')[2])
        return str(year) + "-" + str(month) + "-" + str(last_number+1).zfill(3)
    else:
        return str(year) + "-" + str(month) + "-" + str(1).zfill(3)

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
    bill_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    serial = generate_serial()
    serial_number = forms.CharField(initial=serial, disabled=True)
    class Meta:
        model = OrderPaymentItem
        fields = ['serial_number','payor', 'address', 'fee_type_1', 'fee_type_1_amount', 
                  'fee_type_2', 'fee_type_2_amount', 'fee_type_3', 'fee_type_3_amount',
                  'dst', 'surcharge', 'total_amount', 'amount_in_words', 
                  'bill_no', 'bill_date', 'status', 'bank_name', 'account_number',
                  'deposit_amount']
