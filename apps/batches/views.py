from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.access.services import extend_batch_token
from apps.access.models import TokenAccessAttempt
from apps.access.permissions import has_driver_access_to_batch
from apps.common.enums import BatchStatusChoices
from apps.users.serializers import SignatureCheckMixin

from .permissions import IsEducator, IsProcessor
from .models import WasteBatch
from .serializers import (
    WasteBatchSerializer,
    EducatorBatchCreateSerializer,
    EducatorBatchUpdateSerializer,
    BatchStatusHistorySerializer,
    ExtendTokenSerializer,
    BlockedAttemptSerializer,
)
from .services import create_batch, update_batch, cancel_batch, accept_batch


class EducatorBatchListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WasteBatch.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EducatorBatchCreateSerializer
        return WasteBatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        signature_token = serializer.validated_data.pop('signature_token', None)

        if signature_token:
            if not SignatureCheckMixin.check(request.user, signature_token):
                return Response({'detail': 'Неверный токен подписи'}, status=400)

        batch = create_batch(
            user=request.user,
            validated_data=serializer.validated_data,
            signature_user=request.user
        )

        return Response(WasteBatchSerializer(batch).data, status=201)


class EducatorBatchDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WasteBatch.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return EducatorBatchUpdateSerializer
        return WasteBatchSerializer

    def update(self, request, *args, **kwargs):
        batch = self.get_object()

        serializer = self.get_serializer(instance=batch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data.copy()
        signature_token = data.pop('signature_token', None)

        if signature_token:
            if not SignatureCheckMixin.check(request.user, signature_token):
                return Response({'detail': 'Неверный токен подписи'}, status=400)

        batch = update_batch(batch=batch, user=request.user, data=data)

        return Response(WasteBatchSerializer(batch).data)


class CancelBatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        batch = get_object_or_404(WasteBatch, pk=pk)

        if not SignatureCheckMixin.check(request.user, request.data.get('signature_token', '')):
            return Response({'detail': 'Неверный токен подписи'}, status=400)

        cancel_batch(batch=batch, user=request.user, reason=request.data.get('reason', ''))

        return Response({'detail': 'Партия отменена'})


class ExtendTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        batch = get_object_or_404(WasteBatch, pk=pk)

        serializer = ExtendTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not SignatureCheckMixin.check(request.user, serializer.validated_data.get('signature_token')):
            return Response({'detail': 'Неверный токен подписи'}, status=400)

        token = extend_batch_token(
            batch=batch,
            expires_at=serializer.validated_data.get('expires_at')
        )

        return Response({'expires_at': token.expires_at})


class BatchTimelineView(generics.ListAPIView):
    serializer_class = BatchStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        batch = get_object_or_404(WasteBatch, pk=self.kwargs['pk'])
        return batch.status_history.all()


class BatchBlockedAttemptsView(generics.ListAPIView):
    serializer_class = BlockedAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        batch = get_object_or_404(WasteBatch, pk=self.kwargs['pk'])
        return TokenAccessAttempt.objects.filter(batch=batch, success=False)


class ProcessorBatchListView(generics.ListAPIView):
    serializer_class = WasteBatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WasteBatch.objects.all()


class ProcessorBatchDetailView(generics.RetrieveAPIView):
    serializer_class = WasteBatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WasteBatch.objects.all()


class ProcessorAcceptBatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        batch = get_object_or_404(WasteBatch, pk=pk)

        if not SignatureCheckMixin.check(request.user, request.data.get('signature_token', '')):
            return Response({'detail': 'Неверный токен подписи'}, status=400)

        accept_batch(batch=batch, user=request.user)

        return Response({'detail': 'Партия принята'})
