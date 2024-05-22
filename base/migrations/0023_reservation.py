# Generated by Django 3.1.14 on 2024-04-21 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20240421_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reserved', models.DateTimeField(auto_now_add=True)),
                ('nb_persons', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.post')),
            ],
        ),
    ]
