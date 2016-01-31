# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 06:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0006_baseuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='washer',
        ),
        migrations.AddField(
            model_name='bankaccount',
            name='baseUser',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
