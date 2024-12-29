from rest_framework.test import APIClient, APITestCase
from django.test import TestCase
from movies.models import Movie
from datetime import date
from rest_framework import status


class TestUploadCSVView(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_successful_csv_upload(self):
        url = '/v1/upload-csv/'
        data = {
            "csv_file": "https://d31b0xt3oaqqjh.cloudfront.net/cms-documents/584a0b943291161558cdb39be9dd0a9b00a036b6.csv"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], "CSV uploaded successfully.")

    def test_csv_upload_missing_file(self):
        url = '/v1/upload-csv/'
        data = {}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "No 'csv_file' URL provided in the request body.")

    def test_csv_upload_invalid_url(self):
        url = '/v1/upload-csv/'
        data = {
            "csv_file": "https://invalid-url.com/file.csv"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], "Failed to fetch or parse the CSV content.")


class MovieListViewTestCase(APITestCase):
    def setUp(self):
        # Creating some sample movie data for testing
        Movie.objects.create(
            title="Test Movie 1",
            description="A test movie",
            release_date=date(2020, 5, 10),
            rating=7.5,
            original_language="en",
            budget=100000,
            homepage="https://example.com",
            original_title="Test Movie 1",
            overview="Overview of Test Movie 1",
            revenue=500000,
            runtime=120,
            status="Released",
            vote_average=6.5,
            vote_count=1000,
            production_company_id=1,
            genre_id=1,
            languages=["English"]
        )
        Movie.objects.create(
            title="Test Movie 2",
            description="Another test movie",
            release_date=date(2021, 6, 15),
            rating=8.2,
            original_language="fr",
            budget=150000,
            homepage="https://example.com",
            original_title="Test Movie 2",
            overview="Overview of Test Movie 2",
            revenue=600000,
            runtime=140,
            status="Released",
            vote_average=7.8,
            vote_count=2000,
            production_company_id=2,
            genre_id=2,
            languages=["French"]
        )

    def test_movie_list_with_pagination(self):
        url = '/v1/movies/?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Should return both movies
        self.assertIn('next', response.data)  # Pagination should include next link

    def test_filter_by_year_of_release(self):
        # Test the filter by year functionality
        url = '/v1/movies/?year=2020'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Movie 1")

    def test_filter_by_language(self):
        # Test the filter by language functionality
        url = '/v1/movies/?language=en'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Movie 1")

    def test_sort_by_release_date(self):
        # Test sorting by release_date
        url = '/v1/movies/?sort_by=release_date'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], "Test Movie 1")  # Movie with earlier release date

    def test_sort_by_rating(self):
        # Test sorting by rating (descending order)
        url = '/v1/movies/?sort_by=rating'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], "Test Movie 2")  # Movie with higher rating

    def test_combined_filtering_and_sorting(self):
        # Test combined filtering by year and language, and sorting by rating
        url = '/v1/movies/?year=2021&language=fr&sort_by=rating'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Movie 2")


