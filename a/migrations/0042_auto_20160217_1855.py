# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0041_auto_20160217_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='type',
            field=models.CharField(choices=[('Hatchback', 'Hatchback'), ('Sedan', 'Sedan'), ('Wagon', 'Wagon'), ('SUV', 'SUV'), ('Van', 'Van')], default='Sedan', max_length=10),
        ),
    ]
