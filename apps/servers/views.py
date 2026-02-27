"""
ServerHub — Sunucu View'ları
"""
from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Game, ServerCategory, Server, Vote
from .serializers import (
    GameSerializer, ServerCategorySerializer,
    ServerListSerializer, ServerDetailSerializer, ServerCreateSerializer,
)


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


# ── Oyun ──────────────────────────────────────────────────────

class GameListView(generics.ListAPIView):
    """GET /api/v1/servers/games/"""
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [AllowAny]


# ── Kategori ──────────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """GET /api/v1/servers/categories/?game=<id>"""
    serializer_class = ServerCategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        game_id = self.request.query_params.get('game')
        qs = ServerCategory.objects.all()
        if game_id:
            qs = qs.filter(game_id=game_id)
        return qs


# ── Sunucu ────────────────────────────────────────────────────

class ServerListView(generics.ListAPIView):
    """GET /api/v1/servers/  — filtreleme + arama destekli"""
    serializer_class = ServerListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['vote_count', 'created_at', 'exp_rate']
    ordering = ['-is_premium', '-vote_count']

    def get_queryset(self):
        qs = Server.objects.filter(status=Server.STATUS_APPROVED)
        game_id     = self.request.query_params.get('game')
        category_id = self.request.query_params.get('category')
        if game_id:
            qs = qs.filter(game_id=game_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs


class ServerCreateView(generics.CreateAPIView):
    """POST /api/v1/servers/create/"""
    serializer_class = ServerCreateSerializer
    permission_classes = [IsAuthenticated]


class ServerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/DELETE /api/v1/servers/<slug>/"""
    queryset = Server.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ServerCreateSerializer
        return ServerDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user and not request.user.is_staff:
            return Response({'detail': 'Yetkisiz işlem.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner != request.user and not request.user.is_staff:
            return Response({'detail': 'Yetkisiz işlem.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


# ── Oylama ────────────────────────────────────────────────────

class VoteView(APIView):
    """POST /api/v1/servers/<slug>/vote/"""
    permission_classes = [AllowAny]

    def post(self, request, slug):
        try:
            server = Server.objects.get(slug=slug, status=Server.STATUS_APPROVED)
        except Server.DoesNotExist:
            return Response({'detail': 'Sunucu bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        ip = get_client_ip(request)

        # Aynı IP dün oy kullandıysa sıfırla (günlük oy)
        today = timezone.now().date()
        existing = Vote.objects.filter(server=server, ip_address=ip).first()
        if existing:
            if existing.voted_at.date() < today:
                existing.delete()  # Dünkü oy — sil, yeni oy ver
            else:
                return Response({'detail': 'Bugün zaten oy kullandınız.', 'voted': True},
                                status=status.HTTP_200_OK)

        Vote.objects.create(
            server=server,
            ip_address=ip,
            user=request.user if request.user.is_authenticated else None,
        )
        Server.objects.filter(pk=server.pk).update(vote_count=server.vote_count + 1)
        server.refresh_from_db()
        return Response({'detail': 'Oy kaydedildi!', 'vote_count': server.vote_count},
                        status=status.HTTP_201_CREATED)


class MyServersView(generics.ListAPIView):
    """GET /api/v1/servers/my/  — giriş yapmış kullanıcının sunucuları"""
    serializer_class = ServerListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Server.objects.filter(owner=self.request.user)
