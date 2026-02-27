"""
ServerHub — Scraper Log Modeli
"""
from django.db import models


class ScrapeLog(models.Model):
    """Scraper çalışma geçmişi."""
    source_url   = models.URLField()
    servers_found = models.PositiveIntegerField(default=0)
    servers_new   = models.PositiveIntegerField(default=0)
    status       = models.CharField(max_length=20, default='ok')
    error_msg    = models.TextField(blank=True)
    ran_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Scrape Log'
        verbose_name_plural = 'Scrape Logları'
        ordering = ['-ran_at']

    def __str__(self):
        return f'{self.ran_at:%Y-%m-%d %H:%M} — {self.source_url} ({self.servers_found} sunucu)'
