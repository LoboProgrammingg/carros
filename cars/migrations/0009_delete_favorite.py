# Generated by Django 5.0.6 on 2024-07-11 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_favorite'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]