from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'server_count', 'created_at')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('-created_at',)
    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {'fields': ('avatar', 'bio', 'discord_tag')}),
    )
