# Generated by Django 2.0.5 on 2018-06-13 02:11

from django.db import migrations
import uuid


def gen_uuid(apps, schema_editor):
    Collection = apps.get_model("engine", "Collection")
    for row in Collection.objects.all():
        row.collection_id = uuid.uuid4()
        row.save(update_fields=["collection_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("engine", "0011_collection_collection_id"),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop)
    ]
