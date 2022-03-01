from datetime import date

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import RegistrationForm, dayForm

# home page
@login_required(login_url='/login/')
def index(request):
    user = request.user
    context = {'user':user}
    return render(request, 'main/index.html', context)

# list of buttons that send you to a day form
@login_required(login_url='/login/')
def calendar(request):
    context = {}
    thirty = [4, 6, 9, 11]
    thirty_one = [1, 3, 5, 7, 8, 10, 12]
    currentMonth = date.today().month
    currentYear = date.today().year
    # if 30 day month
    if currentMonth in thirty:
        dateList = []
        count = 30
        for x in range(count):
            dateList.append('{day}-{month}-{year}'.format(day=x, month=currentMonth, year=currentYear))
    # if 31 day month
    elif currentMonth in thirty_one:
        dateList = []
        count = 31
        for x in range(count):
            dateList.append('{day}-{month}-{year}'.format(day=x, month=currentMonth, year=currentYear))
    # if february year
    else:
        dateList = []
        # if a leap year (leap years are divisible by 4)
        if currentYear % 4 == 0:
            count = 29
        else:
            count = 28
        for x in range(count):
            dateList.append('{day}-2-{year}'.format(day=x, year=currentYear))
    context["dates"] = dateList
    return render(request, 'main/calendar.html', context)

@login_required(login_url='/login/')
# day_form returns a day form from a specific date if POST method
# or renders a new form for today
def dayForm(request):#, date=None):
    user = request.user
    context = {"user": user}
    if request.method == "POST":
        form = dayForm(request.POST)
        if form.is_valid():
            # process form.cleaned_data
            form.save()
        return HttpResponseRedirect('main/results.html')
    else:
        form = dayForm()
        context = {"form": form}
        #if date:
            
        #else:
    return render(request, 'main/dailyForm.html', context)

def saveForm(request):
    user = request.user
    context = {"user": user}
    if request.method == "POST":
        form = dayForm(request.POST)
        if form.is_valid():
            # process form.cleaned_data
            form.save()
        return HttpResponseRedirect('main/results.html')
    else:
        return redirect('/')


@login_required(login_url='/login/')
def yearReport(request):
    pass

@login_required(login_url='/login/')
def monthReport(request):
    pass

# displays day form, with filled-in values if already submitted
@login_required(login_url='/login/')
def dayReport(request):
    pass

@login_required(login_url='/login/')
def results(request):
    pass

# table with existing assets and recurring
# link to crud assets
# link to crud recurring
# delete button on each
@login_required(login_url='/login/')
def profile(request):
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
            context = {"form": form}
        return render(request, 'registration/register.html', context)
    else:
        return redirect("index")

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("login")