from django_filters import rest_framework as django_filter, filters

from apps.issues.models import Issues


class IssueFilterSet(django_filter.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Issues
        fields = ('title',)
