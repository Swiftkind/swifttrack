# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-19 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_workdiarylog'),
    ]

    operations = [
        migrations.AddField(
            model_name='workdiarylog',
            name='finished_task',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workdiarylog',
            name='hours',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workdiarylog',
            name='issues',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='workdiarylog',
            name='todo_task',
            field=models.TextField(blank=True, null=True),
        ),
    ]
