from django_filters import rest_framework as filters
from movies.models import Movie
from rest_framework.pagination import PageNumberPagination


class MovieFilter(filters.FilterSet):
    release_year = filters.NumberFilter(field_name='release_date', lookup_expr='year')  # Filter by release year
    language = filters.CharFilter(field_name='language', lookup_expr='exact')  # Filter by language

    class Meta:
        model = Movie
        fields = ['release_year', 'language']


class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
