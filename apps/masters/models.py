from django.db import models

from manager_project.core.models import Base


# Create your models here.
class Category(Base):
    name = models.CharField(max_length=50, verbose_name="project_category")
    description = models.TextField(max_length=200, verbose_name="category_description", null=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"