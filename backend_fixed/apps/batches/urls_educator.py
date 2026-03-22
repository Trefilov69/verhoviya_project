from django.urls import path
from .views import EducatorBatchListCreateView

urlpatterns = [
    path('educator/batches/', EducatorBatchListCreateView.as_view()),
]