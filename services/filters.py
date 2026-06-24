from django_filters.rest_framework import FilterSet
import django_filters
from .models import Service

class ServiceFilter(FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Service
        fields = ['category', 'min_price', 'max_price']