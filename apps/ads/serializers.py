from rest_framework import serializers
from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ('id', 'ad_type', 'image', 'link_url', 'title', 'click_count')
