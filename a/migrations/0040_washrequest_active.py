# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0039_auto_20160217_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='washrequest',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
