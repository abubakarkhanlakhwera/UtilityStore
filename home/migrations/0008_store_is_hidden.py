# Generated by Django 5.1.1 on 2024-09-30 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_alter_items_details_alter_items_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="store",
            name="is_hidden",
            field=models.BooleanField(default=False),
        ),
    ]
