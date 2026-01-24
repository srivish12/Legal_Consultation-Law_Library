from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
path('', views.subscription_list, name='list'),
path('checkout/<str:plan>/', views.subscription_checkout, name='checkout'),
path('renew/<str:plan>/', views.renew_subscription, name='renew'),
path('my_subscription/', views.my_subscription, name='my_subscription'),

]