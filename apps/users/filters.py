from django_filters import rest_framework as django_filter, filters

from apps.users.models import UserProfile


class UserFilterSet(django_filter.FilterSet):
    username = filters.CharFilter(field_name="username", lookup_expr='icontains')
    mobile = filters.CharFilter(field_name="mobile", lookup_expr="icontains")
    is_active = filters.CharFilter(field_name='is_active', lookup_expr="exact")

    class Meta:
        model = UserProfile
        fields = {
            "username": ['icontains'],
            "mobile": ['icontains'],
            "is_active": ['exact']
        }