"""
ServerHub — Reklam View'ları
"""
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ad
from .serializers import AdSerializer


class ActiveAdListView(generics.ListAPIView):
    """GET /api/v1/ads/?type=banner|sidebar|spotlight"""
    serializer_class = AdSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        today = timezone.now().date()
        qs = Ad.objects.filter(
            is_active=True,
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=today),
        ).filter(
            models.Q(end_date__isnull=True)   | models.Q(end_date__gte=today),
        )
        ad_type = self.request.query_params.get('type')
        if ad_type:
            qs = qs.filter(ad_type=ad_type)
        return qs


class AdClickView(APIView):
    """POST /api/v1/ads/<id>/click/"""
    permission_classes = [AllowAny]

    def post(self, request, pk):
        try:
            ad = Ad.objects.get(pk=pk, is_active=True)
        except Ad.DoesNotExist:
            return Response({'detail': 'Reklam bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        ad.register_click()
        return Response({'link_url': ad.link_url})


# models.Q için import düzeltmesi
from django.db import models
