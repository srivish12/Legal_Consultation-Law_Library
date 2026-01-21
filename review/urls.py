from django.urls import path
from . import views


app_name = 'reviews'


urlpatterns = [
path('package/<int:package_id>/add/', views.add_package_review, name='package_add'),
path('load-more-package-reviews/', views.load_more_package_reviews, name='load_more_package_reviews'),
]