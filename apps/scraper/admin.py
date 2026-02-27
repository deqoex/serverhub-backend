from django.contrib import admin
from .models import ScrapeLog


@admin.register(ScrapeLog)
class ScrapeLogAdmin(admin.ModelAdmin):
    list_display = ('ran_at', 'source_url', 'servers_found', 'servers_new', 'status')
    list_filter = ('status',)
    readonly_fields = ('ran_at',)
