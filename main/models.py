from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE,)
    cash = models.DecimalField(max_digits=12, decimal_places=2, blank=False, default=0)


class daily(models.Model):
    dayId = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=False)
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
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return (str(self.userId) + ' - ' + str(self.date))

    def totalExpenses(self):
        dailyExpenseTotal = self.restExp
        dailyExpenseTotal += self.grocExp
        dailyExpenseTotal += self.gasExp
        dailyExpenseTotal += self.uberExp
        dailyExpenseTotal += self.alcExp
        dailyExpenseTotal += self.barberExp
        dailyExpenseTotal += self.barExp
        dailyExpenseTotal += self.discExp
        return dailyExpenseTotal

    def getSum(self):
        sumTotal = self.totalExpenses()
        sumTotal = self.income - sumTotal
        return sumTotal


class asset(models.Model):
    asset_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    depreciation = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    appreciation = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    acquisition_date = models.DateField(auto_now_add=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.name)

class liability(models.Model):
    liability_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class recurring(models.Model):
    categories = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    recurring_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=categories)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.name)