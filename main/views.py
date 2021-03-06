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

from .models import daily, recurring, asset, liability, Profile
from .forms import RegistrationForm, dailyForm, changeMonthForm, assetForm, recurringForm, liabilitiesForm, profileForm, accountForm

# home page
@login_required(login_url='/login/')
def index(request):
    # get user assets, liabilities
    user = request.user
    assets = asset.objects.filter(userId=user)
    liabilities = liability.objects.filter(userId=user)
    
    try:
        profile = Profile.objects.get(userId=request.user)
        cash = profile.cash
    except:
        return redirect('profile')
    netWorth = cash
    for assetItem in assets:
        netWorth += assetItem.value
    for liaItem in liabilities:
        netWorth -= liaItem.value
    
    # use these variables for querying data based on date
    currentYear = date.today().year
    currentMonth = date.today().month
    currentDay = date.today().day
    templateDate = "{day}-{month}-{year}".format(day=currentDay, month=currentMonth, year=currentYear)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    class monthSummary(object):
        def __init__(self, month, income, expense):
            self.month = month
            self.income = income
            self.expense = expense
            self.sum = self.income - self.expense
            if self.sum < 0:
                self.sum = -self.sum
                # negative sum will be used for comparison in template
                self.negativeSum = True
            else:
                self.negativeSum = False

    # list to append monthSummary objects
    monthObjects = []

    for x in range(len(months)):
        objectMonth = x + 1
        nextMonth = objectMonth + 1
        if currentMonth < objectMonth:
            continue
        # add leading 0 if month is single digit so fromisoformat will work 
        if objectMonth < 10:
            objectMonth = '0' + str(objectMonth)
        else:

            objectMonth = str(objectMonth)
        if nextMonth < 10:
            nextMonth = '0' + str(nextMonth)
        else:
            nextMonth = str(nextMonth)



        # 1st of month datetime object
        firstOfMonth = datetime.fromisoformat("{year}-{month}-01".format(year=currentYear, month=objectMonth))
        # last of month
        lastOfMonth = datetime.fromisoformat("{year}-{month}-01".format(year=currentYear, month=nextMonth))

        # variables to increment; will be added to monthSummary object
        monthlyExpense = 0
        monthlyIncome = 0
        

        #query recurring items
        monthlyRecurringItems = recurring.objects.filter(userId=user)
        if monthlyRecurringItems:
            for item in monthlyRecurringItems:
                if item.category == "Expense":
                    monthlyExpense += item.value
                elif item.category == "Income":
                    monthlyIncome += item.value
                else:
                    monthlyRecurringCost = 0

         # daily object queryset for current month
        monthDailyObjects = daily.objects.filter(date__gte=firstOfMonth).filter(date__lt=lastOfMonth).filter(userId=user)
        # loop through objects and add income and expenses
        for day in monthDailyObjects:
            # sum all income for this month
            monthlyIncome += day.income
            # sum all expenses for this month
            monthlyExpense += day.totalExpenses()
        
        # create monthObjects 
        m = monthSummary(months[x], monthlyIncome, monthlyExpense)
        monthObjects.append(m)

    
     # values for incrementing year total
    currentYearIncome = 0
    currentYearExpenses = 0


    # loop through monthObjects to sum all income & expenses for year
    for month in monthObjects:
        currentYearIncome += month.income
        currentYearExpenses -= month.expense

    currentYearDiff = currentYearIncome - currentYearExpenses
    currentYearExpenses = -currentYearExpenses

    # divide currentYearIncome and currentYearExpenses by len(monthObjects) to get averages
    yearAverageIncome = int(currentYearIncome/len(monthObjects))
    yearAverageExpenses = int(currentYearExpenses/len(monthObjects))
    yearAverageDiff = int(yearAverageIncome - yearAverageExpenses)

    currentYear=str(currentYear)
    context = {"user": user, "templateDate":templateDate, "cash":cash, "assets":assets, "liabilities":liabilities, "netWorth": netWorth, "currentYear":currentYear, "monthObjects":monthObjects, "currentYearIncome":currentYearIncome, "currentYearExpenses":currentYearExpenses, "currentYearDiff":currentYearDiff, "yearAverageIncome":yearAverageIncome, "yearAverageExpenses":yearAverageExpenses, "yearAverageDiff":yearAverageDiff}
    return render(request, 'main/index.html', context)

# list of buttons that send you to a day form
@login_required(login_url='/login/')
def calendar(request, month=str(date.today().month), year=str(date.today().year)):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    templateMonth = months[int(month)-1]
    templateYear = year
    context = {'templateMonth':templateMonth, 'templateYear':templateYear}
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
            dateList.append('{year}-{month}-{day}'.format(day=x, month=currentMonth, year=currentYear))
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
        if int(currentYear) % 4 == 0:
            count = 29
        else:
            count = 28
        for x in range(count):
            x += 1
            if x < 10:
                x = '0' + str(x)
            dateList.append('{year}-02-{day}'.format(day=x, year=currentYear))
    context["dates"] = dateList
    form = changeMonthForm(initial={'month':templateMonth.lower(), 'year':templateYear})
    context["form"] = form
    dailyObjects = []
    monthlyIncome = 0
    monthlyExpense = 0
    for date in dateList:
        dateTimeObj = datetime.fromisoformat("{dateString}".format(dateString=date.rstrip('-')))
        try:
            dailyObject = daily.objects.filter(date=dateTimeObj).get(userId=request.user)
            dailyObjects.append(dailyObject)
            monthlyIncome += dailyObject.income
            monthlyExpense += dailyObject.totalExpenses()
        except:
            dailyObjects.append(date)
    context['dailyObjects'] = dailyObjects
    context['monthlyIncome'] = monthlyIncome
    context['monthlyExpense'] = monthlyExpense
    context['monthlyTotal'] = monthlyIncome - monthlyExpense
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
def dayForm(request, formDate):
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
            # create form instance w form.cleaned_data
            formInstance = form.save(commit=False)
            # if there's an existing daily instance for that day
            # (you're updating the form)
            if daily.objects.filter(date=formDate):
                dailyObject = daily.objects.filter(date=formDate).get(userId=user)
                profile = Profile.objects.get(userId=user)
                #subtract income and expenses before adding updated amounts
                profile.cash -= dailyObject.income
                profile.cash += dailyObject.totalExpenses()
                profile.cash += formInstance.income
                profile.cash -= formInstance.totalExpenses()
                profile.save()
                # delete dailyObject
                dailyObject.delete()
                # recreate object
                formInstance.userId = request.user
                formInstance.date = form_date
                formInstance.save()
                
            else: # if new profile instance
                # populate form with user 
                formInstance.userId = request.user
                formInstance.date = form_date
                # update profile cash balance
                # get profile object
                profile = Profile.objects.get(userId=user)
                profile.cash += formInstance.income
                profile.cash -= formInstance.totalExpenses()
                profile.save()
                # save form
                formInstance.save()
        return redirect('calendar')
    # display form
    else:
        try:
            # passes form with existing instance data
            day = daily.objects.filter(date=form_date).get(userId=request.user)
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
    user = request.user
    profile = Profile.objects.get(userId=user)
    assets = asset.objects.filter(userId=user)
    liabilities = liability.objects.filter(userId=user)
    posRecurringItems = recurring.objects.filter(userId=user).filter(category="Income")
    negRecurringItems = recurring.objects.filter(userId=user).filter(category="Expense")
    netWorth = 0
    assetTotal = profile.cash
    liabilitiesTotal = 0
    recurringTotal = 0
    for assetItem in assets:
        assetTotal += assetItem.value
    for liabilityItem in liabilities:
        liabilitiesTotal += liabilityItem.value
    for recurringItem in negRecurringItems:
        recurringTotal -= recurringItem.value
    for recurringItem in posRecurringItems:
        recurringTotal += recurringItem.value
    context = {"assets":assets, "liabilities":liabilities, "posRecurringItems":posRecurringItems, "negRecurringItems":negRecurringItems, "profile":profile, "netWorth": netWorth, "assetTotal":assetTotal, "liabilitiesTotal":liabilitiesTotal, "recurringTotal":recurringTotal}
    return render(request, 'main/alr.html', context)

@login_required(login_url='/login/')
def createAsset(request):
    context = {}
    if request.method == "POST":
        form = assetForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            formInstance = form.save(commit=False)
            # populate form with user 
            formInstance.userId = request.user
            # save form
            formInstance.save()
        return redirect('A&L')
    else:
        form = assetForm()
        context['form'] = form
        context['urlName'] = 'createAsset'
    return render(request, 'main/assetForm.html', context)

def editAsset(request, assetId=None):
    context = {}
    if request.method == "POST":
        form = assetForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            assetData = form.cleaned_data
            assetObj = asset.objects.get(asset_id=assetId)
            assetObj.name = assetData['name']
            assetObj.value = assetData['value']
            assetObj.appreciation = assetData['appreciation']
            assetObj.depreciation = assetData['depreciation']
            assetObj.save()
        return redirect('A&L')
    else:
        assetInstance = asset.objects.get(asset_id=assetId)
        form = assetForm(instance=assetInstance)
        context['form'] = form
        context['assetInstance'] = assetInstance
    return render(request, 'main/editAsset.html', context)

def deleteAsset(request, assetId=None):
    try:
        # passes form with existing instance data
        assetObj = asset.objects.get(asset_id=assetId)
        assetObj.delete()
    except:
        return redirect('A&L')
    return redirect('A&L')


@login_required(login_url='/login/')
def createLiability(request):
    context = {}
    if request.method == "POST":
        form = liabilitiesForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            formInstance = form.save(commit=False)
            # populate form with user 
            formInstance.userId = request.user
            # save form
            formInstance.save()
        return redirect('A&L')
    else:
        form = liabilitiesForm()
        context['form'] = form
    return render(request, 'main/liabilitiesForm.html', context)

def editLiability(request, liabilityId=None):
    context = {}
    if request.method == "POST":
        form = liabilitiesForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            liabilityData = form.cleaned_data
            liabilityObj = liability.objects.get(liability_id=liabilityId)
            liabilityObj.name = liabilityData['name']
            liabilityObj.value = liabilityData['value']
            liabilityObj.interest = liabilityData['interest']
            liabilityObj.payment = liabilityData['payment']
            liabilityObj.save()
        return redirect('A&L')
    else:
        liabilityInstance = liability.objects.get(liability_id=liabilityId)
        form = liabilitiesForm(instance=liabilityInstance)
        context['form'] = form
        context['liabilityInstance'] = liabilityInstance
    return render(request, 'main/editLiability.html', context)

def deleteLiability(request, liabilityId=None):
    try:
        # passes form with existing instance data
        liabilityObj = liability.objects.get(liability_id=liabilityId)
        liabilityObj.delete()
    except:
        return redirect('A&L')
    return redirect('A&L')












@login_required(login_url='/login/')
def createRecurring(request):
    context = {}
    if request.method == "POST":
        form = recurringForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            formInstance = form.save(commit=False)
            # populate form with user 
            formInstance.userId = request.user
            # save form
            formInstance.save()
        return redirect('A&L')
    else:
        form = recurringForm()
        context['form'] = form
    return render(request, 'main/recurringForm.html', context)

def editRecurring(request, recurringId=None):
    context = {}
    if request.method == "POST":
        form = recurringForm(request.POST)
        if form.is_valid():
            # create form instance w form.cleaned_data
            recurringData = form.cleaned_data
            recurringObj = recurring.objects.get(recurring_id=recurringId)
            recurringObj.name = recurringData['name']
            recurringObj.category = recurringData['category']
            recurringObj.value = recurringData['value']
            recurringObj.save()
        return redirect('A&L')
    else:
        recurringInstance = recurring.objects.get(recurring_id=recurringId)
        form = recurringForm(instance=recurringInstance)
        context['form'] = form
        context['recurringInstance'] = recurringInstance
    return render(request, 'main/editRecurring.html', context)

def deleteRecurring(request, recurringId=None):
    try:
        # passes form with existing instance data
        recurringObj = recurring.objects.get(recurring_id=recurringId)
        recurringObj.delete()
    except:
        return redirect('A&L')
    return redirect('A&L')







# edit username, pw, email
@login_required(login_url='/login/')
def account(request):
    if request.method == "POST":
        form = accountForm(data=request.POST)
        if form.is_valid():
            formInstance.save()
            return redirect("index")
    else:
        form = accountForm(instance=request.user)
    context = {"form": form}
    return render(request, 'main/profile.html', context)
    pass

@login_required(login_url='/login/')
def profileView(request):
    if request.method == "POST":
                form = profileForm(data=request.POST)
                if form.is_valid():
                    if Profile.objects.get(userId=request.user):
                        profileObject = Profile.objects.get(userId=request.user)
                        formCash = form.cleaned_data.get('cash')
                        profileObject.cash = formCash
                        profileObject.save()
                    else:
                        formInstance = form.save(commit=False)
                        formInstance.userId = request.user
                        formInstance.save()
                    return redirect("index")
    else:
        if Profile.objects.get(userId=request.user):
            profileObject = Profile.objects.get(userId=request.user)
            form = profileForm(instance=profileObject)
            value = "Edit Cash Balance"
        else:
            form = profileForm()
            value = "How much cash do you have right now?"
    context = {"form": form, "value": value}
    return render(request, 'main/profile.html', context)

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
                return redirect("profile")
        else:
            form = RegistrationForm()
        return render(request, 'registration/register.html', {"form": form})
    else:
        return redirect("index")

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("login")