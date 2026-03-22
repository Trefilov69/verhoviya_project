from rest_framework.views import APIView
from rest_framework.response import Response


class EducatorBatchListCreateView(APIView):
    def post(self, request):
        return Response({
            "type": request.data.get("type"),
            "quantity": request.data.get("quantity"),
            "unit": request.data.get("unit"),
        }, status=201)