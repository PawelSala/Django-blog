# accounts/admin.py

from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # Wyświetlane pola w listowaniu
    search_fields = ('user__username', 'bio')  # Pola do wyszukiwania

#admin.site.register(Profile)
