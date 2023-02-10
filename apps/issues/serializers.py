from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from rest_framework import status, serializers
from rest_framework.response import Response

from apps.issues.functions import is_project_user
from apps.issues.models import Issues, IssueUser
from apps.projects.models import Project
from manager_project.core.serializers import BaseSerializer


class IssueUserSerializer(BaseSerializer):

    class Meta:
        model = IssueUser
        fields = ('issue', 'assign_to')


class IssueSerializer(BaseSerializer):
    issue_users = IssueUserSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Issues
        fields = (
            "id", "project", "title", "type", "status", "priority", "description", "reported_id",
            'issue_users'
        )
        read_only_fields = ("id", 'issue_users', 'project')

    def validate(self, attrs):
        request = self.context.get('request')
        project_instance = Project.objects.filter(pk=request.data.get('project'))
        if not project_instance:
            raise ValidationError({"error": "Project not Found"})
        return super(IssueSerializer, self).validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')
        with transaction.atomic():
            issue_instance = Issues.objects.create(
                project_id=request.data.get('project'),
                title=validated_data.get('title'),
                status=validated_data.get('status'),
                priority=validated_data.get('priority'),
                type=validated_data.get('type'),
                description=validated_data.get('description'),
                reported_id=validated_data.get('reported_id')
            )
            project_id = issue_instance.project.id
            issue_users = self.context.get('issue_users')
            logged_in_user = request.user
            if issue_users:
                project_user = is_project_user(
                    project_id=project_id,
                    users=issue_users,
                    logged_in_user=logged_in_user
                )
            issue_users_list = []
            if project_user:
                for issue_user in issue_users:
                    issue_users_list.append(IssueUser(issue=issue_instance, assign_to_id=issue_user))
                if issue_users_list:
                    IssueUser.objects.bulk_create(issue_users_list)
            return issue_instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        with transaction.atomic():
            super().update(instance, validated_data)
            project_user = None
            if self.context.get('issue_users'):
                project_user = is_project_user(
                    project_id=instance.project,
                    users=self.context.get('issue_users'),
                    logged_in_user=request.user
                )
            issue_users_list = []
            if project_user:
                IssueUser.objects.filter(issue=instance).delete()
                for issue_user in self.context.get('issue_users'):
                    issue_users_list.append(
                        IssueUser(issue=instance, assign_to_id=issue_user))
                if issue_users_list:
                    IssueUser.objects.bulk_create(issue_users_list)
            return instance

