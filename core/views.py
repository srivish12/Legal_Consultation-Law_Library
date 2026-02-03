from django.shortcuts import render
from django.conf import settings as django_settings

def site_settings(request):
    return {
        "settings": django_settings,
    }


# Create your views here.
