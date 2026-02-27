from django.urls import path
from .views import (
    GameListView, CategoryListView,
    ServerListView, ServerCreateView, ServerDetailView,
    VoteView, MyServersView,
)

urlpatterns = [
    path('',               ServerListView.as_view(),   name='server-list'),
    path('create/',        ServerCreateView.as_view(), name='server-create'),
    path('my/',            MyServersView.as_view(),    name='my-servers'),
    path('games/',         GameListView.as_view(),     name='game-list'),
    path('categories/',    CategoryListView.as_view(), name='category-list'),
    path('<slug:slug>/',        ServerDetailView.as_view(), name='server-detail'),
    path('<slug:slug>/vote/',   VoteView.as_view(),         name='server-vote'),
]
