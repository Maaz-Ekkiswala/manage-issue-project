from rest_framework import serializers

from apps.masters.models import Category
from manager_project.core.serializers import BaseSerializer


class CategorySerializer(BaseSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ("id", "name", "description")