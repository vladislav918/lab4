from django_filters import rest_framework as filters
from .models import Post


class PostFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.NumberFilter(field_name='category__id')

    class Meta:
        model = Post
        fields = ['name', 'category']
