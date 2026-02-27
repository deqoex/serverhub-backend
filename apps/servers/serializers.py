"""
ServerHub — Sunucu Serializer'ları
"""
from rest_framework import serializers
from .models import Game, ServerCategory, Server, Vote


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'slug', 'icon', 'description')


class ServerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerCategory
        fields = ('id', 'name', 'description', 'order')


class ServerListSerializer(serializers.ModelSerializer):
    """Liste sayfası için özet bilgi."""
    game_name     = serializers.CharField(source='game.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Server
        fields = (
            'id', 'name', 'slug', 'banner',
            'game_name', 'category_name', 'owner_username',
            'exp_rate', 'drop_rate', 'max_level', 'open_date',
            'vote_count', 'view_count', 'is_premium', 'status',
            'created_at',
        )


class ServerDetailSerializer(serializers.ModelSerializer):
    """Detay sayfası için tam bilgi."""
    game     = GameSerializer(read_only=True)
    category = ServerCategorySerializer(read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Server
        fields = (
            'id', 'name', 'slug', 'description', 'banner',
            'game', 'category', 'owner_username',
            'website', 'discord_link', 'ip_address',
            'exp_rate', 'drop_rate', 'yang_rate', 'max_level', 'open_date',
            'vote_count', 'view_count', 'is_premium', 'status',
            'created_at', 'updated_at',
        )
        read_only_fields = ('slug', 'vote_count', 'view_count', 'status', 'is_premium', 'owner_username')


class ServerCreateSerializer(serializers.ModelSerializer):
    """Sunucu oluşturma/güncelleme."""
    class Meta:
        model = Server
        fields = (
            'name', 'description', 'banner',
            'game', 'category',
            'website', 'discord_link', 'ip_address',
            'exp_rate', 'drop_rate', 'yang_rate', 'max_level', 'open_date',
        )

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'server', 'voted_at')
        read_only_fields = ('id', 'voted_at')
