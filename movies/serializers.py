from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'language', 'rating',
            'budget', 'homepage', 'original_language', 'original_title',
            'overview', 'revenue', 'runtime', 'status', 'vote_average',
            'vote_count', 'production_company_id', 'genre_id', 'languages'
        ]