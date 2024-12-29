from django_filters import FilterSet, CharFilter
from movies.models import Movie


class MovieFilter(FilterSet):
    release_date = CharFilter(field_name='release_date', lookup_expr='exact')
    original_language = CharFilter(field_name='original_language', lookup_expr='exact')

    class Meta:
        model = Movie
        fields = ['release_date', 'original_language']