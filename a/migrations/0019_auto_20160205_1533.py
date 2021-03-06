# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 05:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0018_washrequest_extra_dirty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='baseUser',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='address',
            name='washRequest',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='a.WashRequest'),
        ),
    ]
