import csv
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from movies.helpers import MovieFilter
from movies.models import Movie
from movies.serializers import MovieSerializer


class UploadCSVView(APIView):

    def post(self, request):
        # Extract CSV file URL from the request data
        csv_file_url = request.data.get('csv_file')

        if not csv_file_url:
            return self._error_response("No 'csv_file' URL provided in the request body.")

        try:
            # Fetch the CSV content from the provided URL
            csv_content = self._fetch_csv(csv_file_url)
            if not csv_content:
                return self._error_response("Failed to fetch or parse the CSV content.")

            # Process the CSV content
            movies = self._process_csv(csv_content)

            if not movies:
                return self._error_response("No valid movie data found in the CSV.")

            # Bulk create Movie objects in the database
            Movie.objects.bulk_create(movies)

            return Response({"message": "CSV uploaded successfully."}, status=status.HTTP_201_CREATED)

        except requests.exceptions.RequestException as e:
            return self._error_response(f"Failed to fetch the file: {e}")

        except Exception as e:
            return self._error_response(str(e))

    def _fetch_csv(self, csv_file_url):
        """Fetch and decode CSV file content from a given URL."""
        try:
            response = requests.get(csv_file_url)
            response.raise_for_status()
            return response.content.decode('utf-8')
        except requests.exceptions.RequestException:
            return None

    def _process_csv(self, csv_content):
        """Process CSV content into Movie objects."""
        movies = []
        csv_reader = csv.reader(csv_content.splitlines())
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            movie = self._create_movie_from_row(row)
            if movie:
                movies.append(movie)

        return movies

    def _create_movie_from_row(self, row):
        """Create a Movie object from a CSV row."""
        try:
            return Movie(
                budget=self._parse_float(row[0], default=0.0),
                homepage=row[1],
                original_language=row[2],
                original_title=row[3],
                overview=row[4],
                release_date=row[5] or None,
                revenue=self._parse_float(row[6]),
                runtime=self._parse_int(row[7]),
                status=row[8],
                title=row[9],
                vote_average=self._parse_float(row[10]),
                vote_count=self._parse_int(row[11]),
                production_company_id=self._parse_int(row[12]),
                genre_id=self._parse_int(row[13]),
                languages=row[14]
            )
        except IndexError:
            return None

    def _parse_float(self, value, default=0.0):
        """Safely parse a string as a float."""
        try:
            return float(value) if value else default
        except ValueError:
            return default

    def _parse_int(self, value, default=0):
        """Safely parse a string as an integer."""
        try:
            return int(float(value)) if value else default  # Convert to float first, then to int
        except ValueError:
            return default

    def _error_response(self, message):
        """Return a standardized error response."""
        return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MovieFilter
    ordering_fields = ['release_date', 'rating']
    ordering = ['-release_date']
