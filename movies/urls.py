from django.urls import path
from movies.views import UploadCSVView, MovieListView

urlpatterns = [
    path('upload-csv/', UploadCSVView.as_view(), name='upload_csv'),
    path('movies/', MovieListView.as_view(), name='list_movies'),
]

