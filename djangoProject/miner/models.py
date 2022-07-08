from django.db import models
# from django.forms import ModelForm

# Create your models here.

class States(models.Model):
    state = models.CharField(max_length=24, unique=True)
    abrv = models.CharField(max_length=2)
    avg_price_per_kwh = models.DecimalField(decimal_places=4, max_digits=10)


class BTCPrices(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=4)
    time = models.TimeField(auto_now=True)

