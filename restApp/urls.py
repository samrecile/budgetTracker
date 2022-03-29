from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'index', views.indexViewSet,basename="index")


urlpatterns = [
    path('', include(router.urls)),
]