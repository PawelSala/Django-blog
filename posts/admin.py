# posts/admin.py

from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Wyświetlane pola w listowaniu
    list_filter = ('author', 'created_at')            # Filtry po prawej stronie
    search_fields = ('title', 'content')             # Pola do wyszukiwania
    ordering = ('-created_at',)                       # Sortowanie domyślne
