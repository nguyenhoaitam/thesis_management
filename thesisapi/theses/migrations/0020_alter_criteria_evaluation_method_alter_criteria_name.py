# Generated by Django 5.0.4 on 2024-05-30 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0019_alter_score_criteria_alter_score_score_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criteria',
            name='evaluation_method',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='criteria',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
