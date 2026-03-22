from django.urls import path
from apps.batches.views import EducatorBatchListCreateView

urlpatterns = [
    path('api/v1/educator/batches', EducatorBatchListCreateView.as_view()),
]