from django.db import models

from apps.issues.constants import Type, Status, Priority
from apps.projects.models import Project
from apps.users.models import UserProfile
from manager_project.core.models import Base


# Create your models here.


class Issues(Base):
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, verbose_name="project_issue"
    )
    title = models.TextField(verbose_name="issue_name")
    type = models.CharField(
        choices=Type.choices(), default=Type.TASK, max_length=6
    )
    status = models.CharField(
        choices=Status.choices(), default=Status.PENDING, max_length=25
    )
    priority = models.CharField(
        choices=Priority.choices(), default=Priority.LOW, max_length=15
    )
    description = models.TextField(blank=True, null=True)
    reported_id = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "issues"
        ordering = ('created_ts', 'priority')


class IssueUser(Base):
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE, related_name="issue_users")
    assign_to = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "issue_users"
        unique_together = ["issue", "assign_to"]


