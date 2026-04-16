from django.contrib import admin
from .models import Lawyer
from .import views
from django.urls import path


urlpatterns = [
    path('search/', views.search_lawyer, name='search_lawyer'),
    path('', views.search_form, name='search_form'),
    path('lawyer/create/', views.create_lawyer, name='create_lawyer'),
    path('lawyer/<int:lawyer_id>/edit/', views.edit_lawyer, name='edit_lawyer'),
    path('lawyer/<int:lawyer_id>/delete/', views.delete_lawyer, name='delete_lawyer'),
    path('lawyer/<slug:slug>/', views.lawyer_details, name='lawyer_details'),

]
