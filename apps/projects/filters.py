from django_filters import rest_framework as django_filter, filters

from apps.projects.models import Project


class ProjectFilterSet(django_filter.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    is_active = filters.CharFilter(field_name="is_active", lookup_expr="exact")

    class Meta:
        model = Project
        fields = ("name", "description", "is_active")