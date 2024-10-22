import django_filters
from django.db.models import Q
import models_database.models


class Product(django_filters.FilterSet):
    price_range = django_filters.RangeFilter(field_name='price', label='Цена от и до')
    available = django_filters.BooleanFilter(method='filter_available', label='В наличии')
    term = django_filters.CharFilter(method='filter_term', label='Поиск')
    category = django_filters.CharFilter(method='filter_category', label='Категория')
    class Meta:
        model = models_database.models.Product
        fields = ['term', 'price_range', 'available', 'category']

    def filter_available(self, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(quantity__gt=0)
        return queryset.filter(quantity=0)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(product_name__icontains=term) |Q(description__icontains=term)
        return queryset.filter(criteria).distinct()

    def filter_category(self, queryset, name, value):
        return queryset.filter(category__category_name__icontains=value)