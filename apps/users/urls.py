from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, UserPublicDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
    path('me/',       ProfileView.as_view(),  name='profile'),
    path('users/<int:pk>/', UserPublicDetailView.as_view(), name='user-detail'),
]
