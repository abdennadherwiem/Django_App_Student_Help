# Generated by Django 3.1.14 on 2024-05-12 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_auto_20240512_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
