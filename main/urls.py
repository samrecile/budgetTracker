from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/<str:month>/<str:year>', views.calendar, name='calendar'),
    path('change_month/', views.changeMonth, name='changeMonth'),
    path('day_form/', views.dayForm, name='dayForm'),
    path('day_form/<str:formDate>/', views.dayForm, name='dayForm'),
    path('A&L/', views.assetsLiabilities, name='A&L'),
    path('changeAsset/', views.changeAsset, name='changeAsset'),
    path('changeAsset/<str:formDate>', views.changeAsset, name='changeAsset'),
    path('changeLiability/', views.changeLiability, name='changeLiability'),
    path('changeLiability/<str:formDate>', views.changeLiability, name='changeLiability'),
    path('changeRecurring/', views.changeRecurring, name='changeRecurring'),
    path('changeRecurring/<str:formDate>', views.changeRecurring, name='changeRecurring'),
]