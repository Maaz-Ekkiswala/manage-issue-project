from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers


from apps.comments.models import Comments
from apps.comments.serializers import CommentSerializer
from apps.issues.models import Issues, IssueUser
from apps.projects.models import Project
from manager_project.core.serializers import BaseSerializer


class IssueUserSerializer(BaseSerializer):

    class Meta:
        model = IssueUser
        fields = ('issue', 'assign_to')


class IssueSerializer(BaseSerializer):
    issue_users = IssueUserSerializer(required=False, many=True, read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issues
        fields = (
            "id", "project", "title", "type", "status", "priority", "description", "reported_id",
            'issue_users', 'comments'
        )
        read_only_fields = ("id", 'issue_users', 'project')

    def validate(self, attrs):
        request = self.context.get('request')
        project_instance = Project.objects.filter(pk=request.query_params.get('project_id'))
        if not project_instance:
            raise ValidationError({"error": "Project not Found"})
        return super(IssueSerializer, self).validate(attrs)

    def create(self, validated_data):
        request = self.context.get('request')
        with transaction.atomic():
            validated_data['project_id'] = request.query_params.get('project_id')
            issue_instance = super().create(validated_data)
            issue_users = self.context.get('issue_users')
            issue_users_list = []
            for issue_user in issue_users:
                issue_users_list.append(IssueUser(issue=issue_instance, assign_to_id=issue_user))
            if issue_users_list:
                IssueUser.objects.bulk_create(issue_users_list)
            return issue_instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            super().update(instance, validated_data)
            issue_users_list = []
            IssueUser.objects.filter(issue=instance).delete()
            for issue_user in self.context.get('issue_users'):
                issue_users_list.append(
                    IssueUser(issue=instance, assign_to_id=issue_user))
            if issue_users_list:
                IssueUser.objects.bulk_create(issue_users_list)
            return instance

    def get_comments(self, instance):
        comments = Comments.objects.filter(issue=instance)
        return CommentSerializer(instance=comments, many=True, read_only=True).data
