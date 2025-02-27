# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=200)),
                ("difficulty", models.FloatField(blank=True, null=True)),
                ("tags", models.TextField(default="")),
                ("type", models.CharField(default="", max_length=200)),
                ("include_adaptive", models.BooleanField(default=True)),
                (
                    "nonadaptive_order",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "preadaptive_order",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("max_problems", models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Confidence",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="EngineSettings",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=200)),
                ("r_star", models.FloatField()),
                ("L_star", models.FloatField()),
                ("W_p", models.FloatField()),
                ("W_r", models.FloatField()),
                ("W_c", models.FloatField()),
                ("W_d", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="ExperimentalGroup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="", max_length=200)),
                ("weight", models.FloatField(default=0)),
                (
                    "engine_settings",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.EngineSettings",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Exposure",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Guess",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.Activity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KnowledgeComponent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("mastery_prior", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Learner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "experimental_group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.ExperimentalGroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Mastery",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                (
                    "knowledge_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.KnowledgeComponent",
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="engine.Learner"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrerequisiteRelation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                (
                    "knowledge_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.KnowledgeComponent",
                    ),
                ),
                (
                    "prerequisite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dependent_relation",
                        to="engine.KnowledgeComponent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.FloatField()),
                ("timestamp", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.Activity",
                    ),
                ),
                (
                    "learner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="engine.Learner"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Slip",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.Activity",
                    ),
                ),
                (
                    "knowledge_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.KnowledgeComponent",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transit",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField()),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.Activity",
                    ),
                ),
                (
                    "knowledge_component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="engine.KnowledgeComponent",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="guess",
            name="knowledge_component",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="engine.KnowledgeComponent",
            ),
        ),
        migrations.AddField(
            model_name="exposure",
            name="knowledge_component",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="engine.KnowledgeComponent",
            ),
        ),
        migrations.AddField(
            model_name="exposure",
            name="learner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="engine.Learner"
            ),
        ),
        migrations.AddField(
            model_name="confidence",
            name="knowledge_component",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="engine.KnowledgeComponent",
            ),
        ),
        migrations.AddField(
            model_name="confidence",
            name="learner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="engine.Learner"
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="collection",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="engine.Collection",
            ),
        ),
        migrations.AddField(
            model_name="activity",
            name="knowledge_components",
            field=models.ManyToManyField(blank=True, to="engine.KnowledgeComponent"),
        ),
    ]
