# Generated by Django 4.0.6 on 2022-09-17 21:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flote',
            name='characteristics',
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.AlterField(
            model_name='flote',
            name='views',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='images/'), blank=True, default=list, size=None),
        ),
    ]