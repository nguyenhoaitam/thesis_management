# Generated by Django 5.0.4 on 2024-05-27 17:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0015_alter_thesis_report_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='report_file',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]