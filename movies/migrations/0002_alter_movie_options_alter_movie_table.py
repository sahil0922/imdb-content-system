# Generated by Django 5.1.4 on 2024-12-28 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movie',
            options={'managed': True, 'ordering': ['-release_date']},
        ),
        migrations.AlterModelTable(
            name='movie',
            table='movies',
        ),
    ]
