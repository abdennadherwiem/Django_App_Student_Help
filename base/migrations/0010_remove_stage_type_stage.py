# Generated by Django 4.1.13 on 2024-04-07 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_eventclub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stage',
            name='type_stage',
        ),
    ]
