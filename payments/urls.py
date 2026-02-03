from django.urls import path
from . import views


app_name = 'payments'

urlpatterns = [
    path('checkout/<int:package_id>/', views.checkout, name='checkout'),
    path('success/<int:payment_id>/', views.payment_success, name='success'),
    path('history/', views.payment_history, name='history'),
    path('delete/<int:payment_id>/', views.payment_delete, name='payment_delete'),
    path('subscription_checkout/<int:payment_id>/', views.subscription_checkout, name='subscription_checkout'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),

]
