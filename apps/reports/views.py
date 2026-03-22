from rest_framework import generics
from rest_framework.views import APIView

from apps.batches.models import WasteBatch
from apps.audits.models import AuditEvent

from .serializers import AuditEventSerializer
from .services import apply_batch_filters, export_batches_csv, export_batches_xlsx


# ✅ lazy import (оставляем)
def get_waste_batch_serializer():
    from apps.batches.serializers import WasteBatchSerializer
    return WasteBatchSerializer


class JournalListView(generics.ListAPIView):

    # ❗ ВАЖНО: не serializer_class = ...
    def get_serializer_class(self):
        return get_waste_batch_serializer()

    def get_queryset(self):
        qs = WasteBatch.objects.select_related(
            'waste_type',
            'creator_org',
            'processor_org',
            'current_driver',
            'access_token'
        ).all()
        return apply_batch_filters(qs, self.request.query_params)


class JournalExportView(APIView):

    def get(self, request):
        qs = apply_batch_filters(WasteBatch.objects.all(), request.query_params)
        fmt = request.query_params.get('format', 'csv')
        return export_batches_xlsx(qs) if fmt == 'xlsx' else export_batches_csv(qs)


class AuditListView(generics.ListAPIView):
    serializer_class = AuditEventSerializer

    def get_queryset(self):
        return AuditEvent.objects.select_related('actor_user').all()