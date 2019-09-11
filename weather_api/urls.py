from django.urls import path
from . import views

urlpatterns = [
    path('average_temperature', views.average_temperature, name='average_temperature'),
]