# Generated by Django 3.2.7 on 2021-09-18 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='Categories',
        ),
    ]