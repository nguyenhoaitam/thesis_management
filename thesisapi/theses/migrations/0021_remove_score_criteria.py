# Generated by Django 5.0.4 on 2024-05-30 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0020_alter_criteria_evaluation_method_alter_criteria_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='criteria',
        ),
    ]
