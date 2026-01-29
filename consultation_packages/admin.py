from django.contrib import admin
from .models import ConsultationPackage

@admin.register(ConsultationPackage)
class ConsultationPackageAdmin(admin.ModelAdmin):
    list_display = ('title','package_type', 'min_price', 'max_price', 'lawyer',)
    list_filter = ('lawyer','package_type',)
   
# Register your models here.

