from datetime import date, datetime

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import daily, recurring, asset
from .forms import RegistrationForm, dailyForm, changeMonthForm, assetForm, recurringForm

# home page
@login_required(login_url='/login/')
def index(request):
    user = request.user
    context = {'user':user}
    return render(request, 'main/index.html', context)

# list of buttons that send you to a day form
@login_required(login_url='/login/')
def calendar(request, month=str(date.today().month), year=str(date.today().year)):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    templateMonth = months[int(month)-1]
    context = {'templateMonth':templateMonth}
    thirty = ['04', '06', '09', 11]
    thirty_one = ['01', '03', '05', '07', '08', 10, 12]
    currentMonth = month
    currentYear = year
    if int(currentMonth) < 10:
        currentMonth = '0' + str(currentMonth)
    # if 30 day month
    if currentMonth in thirty:
        dateList = []
        count = 30
        for x in range(count):
            x += 1
            if x < 10:
                x = '0' + str(x)
            dateList.append('{year}-{month}-{day}-'.format(day=x, month=currentMonth, year=currentYear))
    # if 31 day month
    elif currentMonth in thirty_one:
        dateList = []
        count = 31
        for x in range(count):
            x += 1
            if x < 10:
                x = '0' + str(x)
            dateList.append('{year}-{month}-{day}'.format(day=x, month=currentMonth, year=currentYear))
    # if february year
    else:
        dateList = []
        # if a leap year (leap years are divisible by 4)
        if currentYear % 4 == 0:
            count = 29
        else:
            count = 28
        for x in range(count):
            x += 1
            if x < 10:
                x = '0' + str(x)
            dateList.append('{year}-02-{day}'.format(day=x, year=currentYear))
    context["dates"] = dateList
    form = changeMonthForm
    context["form"] = form
    return render(request, 'main/calendar.html', context)

# use months list index to convert to str(number), with str(year)
# pass as argument to calendar view
def changeMonth(request):
    months = {'january':'1', 'february':'2', 'march':'3', 'april':'4', 'may':'5', 'june':'6', 'july':'7', 'august':'8', 'september':'9', 'october':'10', 'november':'11', 'december':'12'}
    if request.method == "POST":
        form = changeMonthForm(data=request.POST)
        if form.is_valid():
            month = form.cleaned_data["month"]
            year = form.cleaned_data["year"]
    index = months[month]
    year = str(year)
    url = reverse('calendar', kwargs={'month':index, 'year':year})
    return HttpResponseRedirect(url)

@login_required(login_url='/login/')
# day_form returns a day form from a specific date
# or renders a new form for today
def dayForm(request, formDate=str(date.today())):
    # date for header
    templateDate = formDate
    # ensures arg is string
    formDate = str(formDate)
    # converts url arg to datetime for comparison
    form_date = datetime.fromisoformat(formDate).date()
    # checks if date is future date
    if form_date > date.today():
        return redirect('calendar')
    user = request.user
    context = {"user": user, "date": templateDate}
    # handles form submission
    if request.method == "POST":
        form = dailyForm(request.POST)
        if form.is_valid():
            # process form.cleaned_data
            form.save()
        return HttpResponseRedirect('main/results.html')
    # display form
    else:
        try:
            # passes form with existing instance data
            day = daily.objects.get(date=form_date)
            form = dailyForm(instance=day)
            context['form'] = form
        except:
            # passes blank form
            form = dailyForm()
            context['form'] = form
    return render(request, 'main/dailyForm.html', context)


@login_required(login_url='/login/')
def results(request):
    pass

# table with existing assets and recurring
# link to crud assets
# link to crud recurring
# delete button on each
@login_required(login_url='/login/')
def assetsLiabilities(request):
    pass

@login_required(login_url='/login/')
def alForm(request):
    pass

# displays form (populated if edit) to create an asset or recurring item
@login_required(login_url='/login/')
def assetsRecurringForm(request):
    pass

# edit username, pw, email
@login_required(login_url='/login/')
def account(request):
    pass

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    if next is not None:
                        return redirect("index")
                    else:
                        return redirect("index")
        else:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'registration/login.html', context)
    else:
        return redirect("index")

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                return redirect("index")
        else:
            form = RegistrationForm()
        return render(request, 'registration/register.html', {"form": form})
    else:
        return redirect("index")

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("login")