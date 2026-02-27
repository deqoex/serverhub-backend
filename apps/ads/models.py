"""
ServerHub — Reklam Modeli
"""
from django.conf import settings
from django.db import models
from apps.servers.models import Server


class Ad(models.Model):
    """Ücretli reklam ilanı."""

    TYPE_BANNER    = 'banner'
    TYPE_SIDEBAR   = 'sidebar'
    TYPE_SPOTLIGHT = 'spotlight'
    TYPE_CHOICES = [
        (TYPE_BANNER,    'Üst Banner (728x90)'),
        (TYPE_SIDEBAR,   'Yan Panel (300x250)'),
        (TYPE_SPOTLIGHT, 'Öne Çıkan Sunucu'),
    ]

    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    server     = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='ads', null=True, blank=True)
    ad_type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_BANNER)
    image      = models.ImageField(upload_to='ads/', null=True, blank=True)
    link_url   = models.URLField(blank=True)
    title      = models.CharField(max_length=150, blank=True)
    is_active  = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date   = models.DateField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reklam'
        verbose_name_plural = 'Reklamlar'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_ad_type_display()} — {self.title or self.owner.username}'

    def register_click(self):
        Ad.objects.filter(pk=self.pk).update(click_count=models.F('click_count') + 1)
