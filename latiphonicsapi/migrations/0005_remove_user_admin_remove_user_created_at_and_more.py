# Generated by Django 4.1.3 on 2024-08-24 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("latiphonicsapi", "0004_alter_learningsymbol_example_phrases_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="admin",
        ),
        migrations.RemoveField(
            model_name="user",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="user",
            name="updated_at",
        ),
    ]
