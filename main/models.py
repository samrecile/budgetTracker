from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class daily(models.Model):
    dayId = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    income = models.DecimalField(max_digits=8, decimal_places=2)
    restExp = models.DecimalField(max_digits=8, decimal_places=2)
    grocExp = models.DecimalField(max_digits=8, decimal_places=2)
    gasExp = models.DecimalField(max_digits=8, decimal_places=2)
    uberExp = models.DecimalField(max_digits=8, decimal_places=2)
    alcExp = models.DecimalField(max_digits=8, decimal_places=2)
    barberExp = models.DecimalField(max_digits=8, decimal_places=2)
    barExp = models.DecimalField(max_digits=8, decimal_places=2)
    discExp = models.DecimalField(max_digits=8, decimal_places=2)
    stockExp = models.DecimalField(max_digits=8, decimal_places=2)
    cryptoExp = models.DecimalField(max_digits=8, decimal_places=2)
    debtExp = models.DecimalField(max_digits=8, decimal_places=2)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return (str(self.userId) + ' - ' + str(self.date))

class recurring(models.Model):
    categories = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=categories)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField()
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class asset(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    depreciation = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    acquisition_date = models.DateField(auto_now_add=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)
