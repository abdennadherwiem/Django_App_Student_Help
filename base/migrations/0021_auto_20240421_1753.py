# Generated by Django 3.1.14 on 2024-04-21 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20240421_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
