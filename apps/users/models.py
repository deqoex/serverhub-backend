"""
ServerHub — Kullanıcı Modeli
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Genişletilmiş kullanıcı modeli."""
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    discord_tag = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'

    def __str__(self):
        return self.email

    @property
    def server_count(self):
        return self.servers.count()
