# Generated by Django 4.1.3 on 2024-09-19 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("latiphonicsapi", "0012_alter_symbol_picture_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learningsymbol",
            name="video_url",
            field=models.CharField(default="add a video", max_length=1000),
        ),
    ]