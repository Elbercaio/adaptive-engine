# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-13 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("engine", "0005_auto_20180209_0242"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="tags",
            field=models.TextField(blank=True, default=""),
        ),
    ]
