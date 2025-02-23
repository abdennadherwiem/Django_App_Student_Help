# Generated by Django 4.1.13 on 2024-04-08 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_recommandation_texte_delete_st'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_stage', models.IntegerField(choices=[(1, 'Ouvrier'), (2, 'Technicien'), (3, 'PFE')])),
                ('societe', models.CharField(max_length=255)),
                ('duree', models.IntegerField()),
                ('sujet', models.TextField()),
                ('contact_info', models.CharField(max_length=255)),
                ('specialiste', models.CharField(max_length=255)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.post')),
            ],
        ),
    ]
