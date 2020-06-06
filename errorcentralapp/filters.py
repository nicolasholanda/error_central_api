from django_filters import rest_framework as filters

from errorcentralapp.models import ErrorLog


class ErrorLogFilterSet(filters.FilterSet):
    level = filters.CharFilter(field_name='level', lookup_expr='exact')
    source = filters.CharFilter(field_name='source', lookup_expr='icontains')
    environment = filters.CharFilter(field_name='environment', lookup_expr='exact')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = ErrorLog
        fields = ['level', 'environment']
