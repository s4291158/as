# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-22 05:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0046_promocode_discount_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='washer',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
