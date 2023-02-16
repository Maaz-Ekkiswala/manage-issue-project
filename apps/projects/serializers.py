from rest_framework import serializers

from apps.issues.models import Issues
from apps.issues.serializers import IssueSerializer
from apps.masters.serializers import CategorySerializer
from apps.projects.models import Project, ProjectUser
from manager_project.core.serializers import BaseSerializer


class ProjectSerializer(BaseSerializer):

    class Meta:
        model = Project
        fields = ("id", "name", "url", "description", "category")
        read_only_fields = ("id",)


class ProjectUserSerializer(BaseSerializer):

    class Meta:
        model = ProjectUser
        fields = ("id", "project", 'assign_to')
        read_only_fields = ("id",)


class ProjectDetailedSerializer(BaseSerializer):
    category = CategorySerializer(read_only=True)
    users = serializers.SerializerMethodField(read_only=True)
    issues = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ("id", "name", "url", "description", "category", "users", 'issues')
        read_only_fields = ("id",)

    def get_users(self, instance):
        return ProjectUserSerializer(many=True, instance=instance.project_users).data

    def get_issues(self, instance):
        issues = Issues.objects.filter(project=instance)
        return IssueSerializer(many=True, instance=issues).data

