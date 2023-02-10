from django.db import models

from manager_project.core.models import Base


# Create your models here.
class Category(Base):
    name = models.CharField(max_length=50, verbose_name="project_category")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"