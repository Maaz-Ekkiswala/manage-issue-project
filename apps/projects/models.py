from django.db import models

from apps.masters.models import Category
from apps.users.models import UserProfile
from manager_project.core.models import Base


# Create your models here.
class Project(Base):
    name = models.CharField(max_length=50, verbose_name="project_name", unique=True)
    url = models.CharField(max_length=100, verbose_name="project_url")
    description = models.CharField(max_length=250, verbose_name="project_description")
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "project"


class ProjectUser(Base):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="project_users")
    assign_to = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "project_users"
        unique_together = ["project", "assign_to"]
