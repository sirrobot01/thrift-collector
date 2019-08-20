from django.db import models

# Create your models here.

class PaymentModel(models.Model):
    user = models.CharField(max_length=255)
    total = models.IntegerField(blank=True)
    last_payment = models.IntegerField(blank=True, null=True)
    last_payment_date = models.CharField(blank=True, max_length=255, null=True)

    class Meta:
        db_table = 'payment'

