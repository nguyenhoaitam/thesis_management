# Generated by Django 5.0.4 on 2024-05-28 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0016_alter_thesis_report_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesis',
            name='student',
        ),
        migrations.AddField(
            model_name='student',
            name='thesis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='theses.thesis'),
        ),
    ]