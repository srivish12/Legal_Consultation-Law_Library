from django.contrib import admin
from .models import Lawyer


@admin.register(Lawyer)
class LawyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'lawyer_type', 'speciality', 'court_level', 'is_available')
    list_filter = ('lawyer_type', 'speciality', 'court_level', 'is_available')
    search_fields = ('name', 'email', 'phone')