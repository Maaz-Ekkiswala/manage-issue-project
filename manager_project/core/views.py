from django.db import transaction
from rest_framework import viewsets


class BaseViewSet(viewsets.GenericViewSet):
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        with transaction.atomic():
            instance = serializer.save(updated_by=self.request.user)
