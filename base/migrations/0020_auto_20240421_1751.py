# Generated by Django 3.1.14 on 2024-04-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20240421_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
