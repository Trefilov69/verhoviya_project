from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response


class DummyLoginView(APIView):
    def post(self, request):
        return Response({"token": "test"})


urlpatterns = [
    path('login', DummyLoginView.as_view()),
]