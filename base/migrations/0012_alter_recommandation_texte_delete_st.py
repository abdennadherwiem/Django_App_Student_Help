# Generated by Django 4.1.13 on 2024-04-08 13:05

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_st_delete_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommandation',
            name='texte',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='St',
        ),
    ]
