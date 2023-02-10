from django.db import transaction
from rest_framework import serializers

from apps.masters.serializers import CategorySerializer
from apps.projects.models import Project, ProjectUser
from manager_project.core.serializers import BaseSerializer


class ProjectSerializer(BaseSerializer):

    class Meta:
        model = Project
        fields = ("id", "name", "url", "description", "category")
        read_only_fields = ("id",)


class ProjectUserListSerializer(BaseSerializer):

    class Meta:
        model = ProjectUser
        fields = ("id", "project", 'assign_to')
        read_only_fields = ("id",)


class ProjectDetailedSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)
    project_users = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "url", "description", "category", "project_users")
        read_only_fields = ("id",)

    def get_project_users(self, instance):
        return ProjectUserListSerializer(many=True, instance=instance.project_users).data


class ProjectUserSerializer(BaseSerializer):

    class Meta:
        model = ProjectUser
        fields = ("id", "project", 'assign_to')
        read_only_fields = ("id",)

