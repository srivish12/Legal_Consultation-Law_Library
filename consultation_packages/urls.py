from django.urls import path
from . import views


urlpatterns = [
    path('', views.package_list, name='package_list'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
    path('create/', views.create_package, name='create_package'),

]
