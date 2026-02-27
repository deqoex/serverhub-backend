"""
ServerHub — Kullanıcı Serializer'ları
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Şifreyi Onayla')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Şifreler eşleşmiyor.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UserPublicSerializer(serializers.ModelSerializer):
    """Herkese açık kullanıcı bilgisi."""
    server_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'bio', 'discord_tag', 'server_count', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    """Giriş yapmış kullanıcının kendi profili."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'bio', 'discord_tag', 'created_at')
        read_only_fields = ('id', 'email', 'created_at')
