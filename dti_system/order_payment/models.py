from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OrderPaymentItem(models.Model):

    # header
    entity_name = models.CharField(max_length=200, default="Departmenf of Trade and Industry Region IV-A")
    fund_cluster = models.CharField(max_length=200, default="01-Regular Agency Fund")
    serial_number = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    # collecting officer
    collecting_officer = models.CharField(max_length=200, default="Cash/Treasury Unit")

    # main details
    payor = models.CharField(max_length=200)
    address = models.CharField(max_length=400)
    fee_type_1 = models.CharField(max_length=200)
    fee_type_1_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type_2 = models.CharField(max_length=200, null=True, blank=True)
    fee_type_2_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fee_type_3 = models.CharField(max_length=200, null=True, blank=True)
    fee_type_3_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dst = models.DecimalField(max_digits=10, decimal_places=2)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=500)
    bill_no = models.CharField(max_length=200)
    bill_date = models.DateField(auto_now_add=False)
    status = models.CharField(max_length=200, default="NEW")

    # bank details
    bank_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # approver
    acting_accountant = models.CharField(max_length=200)

    # tags
    update_date = models.DateField(auto_now_add=True)
    last_update_by = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Order Of Payment Items"

    def __str__(self):
        return self.serial_number
