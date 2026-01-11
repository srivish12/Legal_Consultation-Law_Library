from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'final_amount', 'status', 'created_at')
    list_filter = ('status',)