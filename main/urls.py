from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/<str:month>/<str:year>', views.calendar, name='calendar'),
    path('change_month/', views.changeMonth, name='changeMonth'),
    path('day_form/', views.dayForm, name='dayForm'),
    path('day_form/<str:formDate>/', views.dayForm, name='dayForm'),
    path('A&L/', views.assetsLiabilities, name='A&L'),
    path('createAsset/', views.createAsset, name='createAsset'),
    path('editAsset/<int:assetId>', views.editAsset, name='editAsset'),
    path('deleteAsset/<int:assetId>', views.deleteAsset, name='deleteAsset'),
    path('createLiability/', views.createLiability, name='createLiability'),
    path('editLiability/<int:liabilityId>', views.editLiability, name='editLiability'),
    path('deleteLiability/<int:liabilityId>', views.deleteLiability, name='deleteLiability'),
    path('createRecurring/', views.createRecurring, name='createRecurring'),
    path('editRecurring/<int:recurringId>', views.editRecurring, name='editRecurring'),
    path('deleteRecurring/<int:recurringId>', views.deleteRecurring, name='deleteRecurring'),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('profile/', views.profileView, name='profile'),
]