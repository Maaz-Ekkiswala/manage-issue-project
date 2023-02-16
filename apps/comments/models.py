from django.db import models

from apps.issues.models import Issues
from apps.users.models import UserProfile
from manager_project.core.models import Base


# Create your models here.
class Comments(Base):
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="comment_body")

    def __str__(self):
        return self.description

    class Meta:
        db_table = "comments"
        ordering = ('created_ts', )