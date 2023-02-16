from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet


class BaseQuerySet(QuerySet):
    def deactivate(self, user):
        return super(BaseQuerySet, self).update(is_active=False, updated_by=user)

    def activate(self, user):
        return super(BaseQuerySet, self).update(is_active=True, updated_by=user)

    def hard_delete(self):
        return super(BaseQuerySet, self).delete()


class BaseManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.active_only:
            return BaseQuerySet(self.model).filter(is_active=True)
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class Base(models.Model):
    created_ts = models.DateTimeField("Created Date", auto_now_add=True)
    updated_ts = models.DateTimeField("Last Updated Date", auto_now=True)
    created_by = models.ForeignKey(
        User, related_name='%(app_label)s_%(class)s_created_related', null=True, blank=True,
        on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name='%(app_label)s_%(class)s_updated_related', null=True,
        blank=True, on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    objects = BaseManager()
    all_objects = BaseManager(active_only=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(Base, self).save(*args, **kwargs)