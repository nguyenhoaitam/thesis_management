# Generated by Django 5.0.4 on 2024-06-12 06:23

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0023_alter_score_thesis_criteria_post_like_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='report_file',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True),
        ),
    ]
