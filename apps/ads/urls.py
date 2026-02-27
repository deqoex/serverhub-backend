from django.urls import path
from .views import ActiveAdListView, AdClickView

urlpatterns = [
    path('',            ActiveAdListView.as_view(), name='ad-list'),
    path('<int:pk>/click/', AdClickView.as_view(), name='ad-click'),
]
