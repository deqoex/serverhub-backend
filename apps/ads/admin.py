from django.contrib import admin
from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'ad_type', 'is_active', 'start_date', 'end_date', 'click_count')
    list_filter = ('ad_type', 'is_active')
    search_fields = ('title', 'owner__email')
