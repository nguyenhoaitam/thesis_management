# Generated by Django 5.0.4 on 2024-05-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0009_remove_thesis_lecturers_delete_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='thesis',
            name='lecturers',
            field=models.ManyToManyField(blank=True, null=True, to='theses.lecturer'),
        ),
    ]