from django.contrib import admin
from .models import Lawyer
from .import views
from django.urls import path

urlpatterns = [
    path('search/', views.search_lawyer, name='search_lawyer'),
    path('', views.search_form, name='search_form'),
    path('<int:lawyer_id>/', views.lawyer_details, name='lawyer_details'),
    
]