# Generated by Django 3.1.14 on 2024-04-28 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_reservationhistory_transport'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='trasnport',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.transport'),
        ),
    ]
