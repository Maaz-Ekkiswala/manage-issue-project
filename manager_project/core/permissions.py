from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from apps.issues.models import IssueUser
from apps.projects.models import ProjectUser


class ProjectUserPermission(BasePermission):
    def has_permission(self, request, view):
        project_id = request.query_params.get('project_id')
        if not project_id:
            raise ValidationError({"message": "You should pass project_id in parameters"})
        project_users = None
        if project_id:
           project_users = ProjectUser.objects.filter(
               project_id=project_id
           ).values_list('assign_to__id', flat=True)
        users = request.data.get('issue_users')
        if users and project_users:
            if set(users).issubset(set(project_users)):
                return True
            return False
        elif request.user.id in list(project_users):
            return True
        return False


class IssueUserPermission(BasePermission):

    def has_permission(self, request, view):
        issue_id = request.query_params.get('issue_id')
        if not issue_id:
            raise ValidationError({"message": "You should pass issue_id in parameters"})
        issue_users = None
        if issue_id:
            issue_users = IssueUser.objects.filter(
                issue_id=issue_id
            ).values_list('assign_to__id', flat=True)
        if issue_users:
            if request.user.id in list(issue_users):
                return True
        return False
