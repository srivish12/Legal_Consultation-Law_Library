from django.contrib import admin
from .models import Lawyer
from .import views
from django.urls import path

urlpatterns = [
    path('', views.search_lawyer, name='search_lawyer'),

]