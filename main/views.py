from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import RegistrationForm

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

def index(request):
    user = request.user
    context = {'user':user}
    return render(request, 'main/index.html', context)