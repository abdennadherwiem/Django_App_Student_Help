# Generated by Django 3.1.14 on 2024-04-27 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_auto_20240422_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transport',
            name='reserved_seats',
            field=models.IntegerField(default=0),
        ),
    ]
