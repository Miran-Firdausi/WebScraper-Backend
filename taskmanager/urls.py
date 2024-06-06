from django.urls import path
from .views import StartScrapingView, ScrapingStatusView

urlpatterns = [
    path('start_scraping', StartScrapingView.as_view()),
    path('scraping_status/<uuid:job_id>', ScrapingStatusView.as_view()),
]
