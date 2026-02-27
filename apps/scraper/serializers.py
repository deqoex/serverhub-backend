from rest_framework import serializers
from .models import ScrapeLog


class ScrapeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapeLog
        fields = ('id', 'source_url', 'servers_found', 'servers_new', 'status', 'error_msg', 'ran_at')
