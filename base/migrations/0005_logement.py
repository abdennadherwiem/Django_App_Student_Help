# Generated by Django 4.1.13 on 2024-04-06 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_transport'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localisation', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('contact_info', models.CharField(max_length=255)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.post')),
            ],
        ),
    ]
