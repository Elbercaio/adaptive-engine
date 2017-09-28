# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-22 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0009_auto_20170921_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enginesettings',
            name='M',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='epsilon',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='eta',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='guess_probability',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='prior_knowledge_probability',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='slip_probability',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='stop_on_mastery',
        ),
        migrations.RemoveField(
            model_name='enginesettings',
            name='trans_probability',
        ),
        migrations.AlterField(
            model_name='enginesettings',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]