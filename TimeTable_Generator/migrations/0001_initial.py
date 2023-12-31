# Generated by Django 4.2.4 on 2023-08-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20, unique=True)),
                ('course_name', models.CharField(max_length=20)),
                ('slot', models.CharField(max_length=20)),
                ('room', models.CharField(max_length=20)),
                ('discipline', models.CharField(max_length=20)),
                ('instructor', models.CharField(max_length=20)),
            ],
        ),
    ]
