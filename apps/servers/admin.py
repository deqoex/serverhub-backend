from django.contrib import admin
from .models import Game, ServerCategory, Server, Vote


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServerCategory)
class ServerCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'order')
    list_filter = ('game',)


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'game', 'category', 'status', 'is_premium', 'vote_count', 'created_at')
    list_filter = ('status', 'game', 'is_premium')
    search_fields = ('name', 'owner__email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('vote_count', 'view_count', 'created_at', 'updated_at')
    actions = ['approve_servers', 'reject_servers']

    @admin.action(description='Seçili sunucuları onayla')
    def approve_servers(self, request, queryset):
        queryset.update(status=Server.STATUS_APPROVED)

    @admin.action(description='Seçili sunucuları reddet')
    def reject_servers(self, request, queryset):
        queryset.update(status=Server.STATUS_REJECTED)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('server', 'ip_address', 'user', 'voted_at')
    list_filter = ('server',)
