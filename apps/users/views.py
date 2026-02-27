"""
ServerHub — Kullanıcı View'ları
"""
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserPublicSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/v1/auth/register/"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST /api/v1/auth/login/"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail': 'Hatalı e-posta veya şifre.'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
        })


class LogoutView(APIView):
    """POST /api/v1/auth/logout/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Başarıyla çıkış yapıldı.'})


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET/PUT /api/v1/auth/me/"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserPublicDetailView(generics.RetrieveAPIView):
    """GET /api/v1/auth/users/<id>/"""
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [AllowAny]
