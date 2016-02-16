# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 02:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_email_max_length'),
        ('admin', '0002_logentry_remove_auto_add'),
        ('socialaccount', '0002_token_max_lengths'),
        ('a', '0027_auto_20160215_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='washee',
            name='baseuser_ptr',
        ),
        migrations.RemoveField(
            model_name='washer',
            name='baseuser_ptr',
        ),
        migrations.DeleteModel(
            name='Washee',
        ),
        migrations.DeleteModel(
            name='Washer',
        ),
    ]