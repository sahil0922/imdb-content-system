from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    release_date = models.DateField(null=True)
    rating = models.FloatField(default=0.0)
    budget = models.FloatField(default=0.0)
    homepage = models.TextField(null=True)
    original_language = models.CharField(max_length=50, null=True)
    original_title = models.CharField(max_length=255, null=True)
    overview = models.TextField(null=True)
    revenue = models.FloatField(default=0.0)
    runtime = models.IntegerField(default=0)
    status = models.CharField(max_length=50, null=False)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    production_company_id = models.IntegerField(null=True)
    genre_id = models.IntegerField(default=0)
    languages = models.JSONField(null=True)

    class Meta:
        managed = True
        db_table = 'movies'

    def __str__(self):
        return self.title
