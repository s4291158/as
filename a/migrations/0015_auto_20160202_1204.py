# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-02 02:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0014_auto_20160202_0128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='type',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]