# Generated by Django 3.2.7 on 2021-09-18 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Data', models.CharField(default='', max_length=1000000)),
                ('Categories', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app1.datastore')),
            ],
        ),
    ]