# Generated by Django 5.0.4 on 2024-05-25 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0010_thesis_lecturers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thesis',
            name='council',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='theses.council'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')], max_length=10),
        ),
    ]
