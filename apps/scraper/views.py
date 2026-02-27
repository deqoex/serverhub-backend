"""
ServerHub — Scraper View'ları (Admin only)
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScrapeLog
from .serializers import ScrapeLogSerializer


class ScrapeLogListView(generics.ListAPIView):
    """GET /api/v1/scraper/logs/"""
    queryset = ScrapeLog.objects.all()[:50]
    serializer_class = ScrapeLogSerializer
    permission_classes = [IsAdminUser]


class TriggerScrapeView(APIView):
    """POST /api/v1/scraper/run/  — manuel tetikleme"""
    permission_classes = [IsAdminUser]

    def post(self, request):
        from .tasks import run_scraper
        url = request.data.get('url', '')
        if url:
            run_scraper(url)
        else:
            run_scraper()
        return Response({'detail': 'Scraper çalıştırıldı.'}, status=status.HTTP_200_OK)
