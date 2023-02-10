from rest_framework import status
from rest_framework.response import Response

from apps.projects.models import ProjectUser


def is_project_user(project_id, users, logged_in_user):
    project_users = ProjectUser.objects.filter(
        project=project_id
    ).values_list('assign_to__id', flat=True)
    issue_users = []
    for user in users:
        issue_users.append(user)
    admin_user = logged_in_user.is_superuser
    if not admin_user or (
            logged_in_user and issue_users not in list(project_users)
    ):
        return False
    return True