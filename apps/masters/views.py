from django.shortcuts import render
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.masters import serializers, models
from manager_project.core.views import BaseViewSet


# Create your views here.
class CategoryViewSet(BaseViewSet, mixins.ListModelMixin):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = [IsAdminUser]
