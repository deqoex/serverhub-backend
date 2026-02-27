from django.urls import path
from .views import ScrapeLogListView, TriggerScrapeView

urlpatterns = [
    path('logs/', ScrapeLogListView.as_view(), name='scrape-logs'),
    path('run/',  TriggerScrapeView.as_view(), name='scrape-run'),
]
