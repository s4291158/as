# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 02:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a', '0025_washrequest_car_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='washrequest',
            name='assigned_washer',
        ),
        migrations.AddField(
            model_name='washrequest',
            name='washer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_washer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='washrequest',
            name='washee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_washee', to=settings.AUTH_USER_MODEL),
        ),
    ]
