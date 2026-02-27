"""
ServerHub — Ana URL yapılandırması
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/',    include('apps.users.urls')),
    path('api/v1/servers/', include('apps.servers.urls')),
    path('api/v1/ads/',     include('apps.ads.urls')),
    path('api/v1/scraper/', include('apps.scraper.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
