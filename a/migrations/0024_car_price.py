# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 01:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0023_auto_20160208_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
