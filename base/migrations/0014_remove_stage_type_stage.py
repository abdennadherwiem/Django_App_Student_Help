# Generated by Django 4.1.13 on 2024-04-08 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='type_stage',
        ),
    ]
