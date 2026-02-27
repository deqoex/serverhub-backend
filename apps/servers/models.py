"""
ServerHub — Sunucu Listeleme Modelleri
"""
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Game(models.Model):
    """Oyun (şimdilik Metin2, ileride genişletilebilir)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    icon = models.ImageField(upload_to='games/icons/', null=True, blank=True)
    banner = models.ImageField(upload_to='games/banners/', null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Oyun'
        verbose_name_plural = 'Oyunlar'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServerCategory(models.Model):
    """Sunucu kategorisi (65-250, 1-99, Wslik vb.)."""
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'
        ordering = ['order', 'name']
        unique_together = ('game', 'name')

    def __str__(self):
        return f'{self.game.name} — {self.name}'


class Server(models.Model):
    """Oyun sunucusu ilanı."""

    STATUS_PENDING  = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING,  'Onay Bekliyor'),
        (STATUS_APPROVED, 'Yayında'),
        (STATUS_REJECTED, 'Reddedildi'),
    ]

    owner    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='servers')
    game     = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='servers')
    category = models.ForeignKey(ServerCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='servers')

    name        = models.CharField(max_length=150)
    slug        = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    banner      = models.ImageField(upload_to='servers/banners/', null=True, blank=True)

    # Teknik bilgiler
    website       = models.URLField(blank=True)
    discord_link  = models.URLField(blank=True)
    ip_address    = models.CharField(max_length=100, blank=True)
    exp_rate      = models.PositiveIntegerField(default=1, help_text='Deneyim çarpanı')
    drop_rate     = models.PositiveIntegerField(default=1, help_text='Drop çarpanı')
    yang_rate     = models.PositiveIntegerField(default=1, help_text='Yang çarpanı')
    max_level     = models.PositiveIntegerField(default=120)
    open_date     = models.DateField(null=True, blank=True, help_text='Açılış tarihi')

    # İstatistikler
    vote_count   = models.PositiveIntegerField(default=0, editable=False)
    view_count   = models.PositiveIntegerField(default=0, editable=False)

    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    is_premium = models.BooleanField(default=False, help_text='Premium ilan (üstte gösterilir)')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sunucu'
        verbose_name_plural = 'Sunucular'
        ordering = ['-is_premium', '-vote_count', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Server.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def increment_view(self):
        Server.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)


class Vote(models.Model):
    """Oylaması: her IP günde 1 oy."""
    server     = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='votes')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='votes')
    ip_address = models.GenericIPAddressField()
    voted_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Oy'
        verbose_name_plural = 'Oylar'
        # Aynı IP'den aynı sunucuya aynı gün sadece 1 oy
        unique_together = ('server', 'ip_address')

    def __str__(self):
        return f'{self.ip_address} → {self.server.name}'
