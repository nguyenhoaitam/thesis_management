# Generated by Django 5.0.4 on 2024-04-23 15:46

import ckeditor.fields
import cloudinary.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', ckeditor.fields.RichTextField()),
                ('is_block', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('fac_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('start_year', models.DateField()),
                ('end_year', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ScoreComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('evaluation_method', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dkmurrwq5/image/upload/v1713421473/user.png', max_length=255)),
                ('phone', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('male', 'Nam'), ('female', 'Nữ')], max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.role')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('lec_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('maj_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('mi_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50)),
                ('content', ckeditor.fields.RichTextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CouncilDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('council', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.council')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.lecturer')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.position')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('council_detail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.councildetail')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreColumn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('weight', models.FloatField()),
                ('score_component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.scorecomponent')),
            ],
        ),
        migrations.CreateModel(
            name='ScoreDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_number', models.FloatField()),
                ('score', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.score')),
                ('score_column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.scorecolumn')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('stu_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('gpa', models.FloatField()),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.major')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('the_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('report_file', ckeditor.fields.RichTextField(null=True)),
                ('total_score', models.FloatField(default=0, null=True)),
                ('result', models.BooleanField(default=False)),
                ('council', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.council')),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.major')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.schoolyear')),
                ('students', models.ManyToManyField(null=True, to='theses.student')),
            ],
        ),
        migrations.AddField(
            model_name='score',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theses.thesis'),
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.lecturer')),
                ('thesis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='theses.thesis')),
            ],
        ),
    ]
