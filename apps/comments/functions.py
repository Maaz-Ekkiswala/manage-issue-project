from apps.issues.models import IssueUser


def is_issue_user(issue_id, logged_in_user):
    issue_users = IssueUser.objects.filter(
        issue=issue_id
    ).values_list('assign_to__id', flat=True)
    admin_user = logged_in_user.is_superuser
    if admin_user or (
            logged_in_user not in list(issue_users)
    ):
        return True
    return False