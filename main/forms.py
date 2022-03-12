from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['email']

        if commit:
            user.save()
        
        return User

class profileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['cash']


class dailyForm(ModelForm):
    class Meta:
        model = daily
        fields = ['income', 'restExp', 'grocExp', 'gasExp', 'uberExp', 'alcExp', 'barberExp', 'barExp', 'discExp', 'stockExp', 'cryptoExp', 'debtExp']
        #labels = {
        #    "mainInc": "How much money did you make from your main job?", "otherInc":"How much other income did you make?", "gasExp":"How much did you spend on gas?", "uberExp":"How much did you spend on Ubers?", "grocExp":"How much did you spend on groceries?", "restExp":"How much did you spend at restaurants?", "alcExp":"How much did you spend on alcohol?", "personalExp":"How much did you spend on personal expenses (toiletries, etc.)?", "barberExp": "How much did you spend on haircuts?", "barExp":"How much did you spend at bars?", "nightExp":"How much did you spend on other nights out?", "discExp":"How much did you spend on other discretionary expenses (clothes, games)?", "stockExp":"How much did you invest in stocks?", "cryptoExp":"How much did you invest in crypto?", "debtExp": "How much debt did you pay down?",
        #}


class changeMonthForm(forms.Form):
    month_choices = [
        ('january', 'January'),
        ('february', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('june', 'June'),
        ('july', 'July'),
        ('august', 'August'),
        ('september', 'September'),
        ('october', 'October'),
        ('november', 'November'),
        ('december', 'December'),
    ]

    month=forms.CharField(label='Pick a month', widget=forms.Select(choices=month_choices))
    year=forms.IntegerField(label='Pick a year', min_value=2015, max_value=2050)


class assetForm(ModelForm):
    class Meta:
        model = asset
        fields = ['name', 'value', 'depreciation', 'appreciation']

class recurringForm(ModelForm):
    class Meta:
        model = recurring
        fields = ['name', 'category', 'value']
        

class liabilitiesForm(ModelForm):
    class Meta:
        model = liability
        fields = ['name', 'value', 'interest', 'payment']