from django.contrib import admin
from .models import LawBook


@admin.register(LawBook)
class LawBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'subject', 'alphabet')
    search_fields = ('title', 'author', 'subject')
    list_filter = ('subject', 'alphabet')