# Generated by Django 5.0.4 on 2024-05-23 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theses', '0003_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
