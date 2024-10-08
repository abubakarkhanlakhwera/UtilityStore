# Generated by Django 5.1.1 on 2024-09-26 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_alter_store_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="contact_phone",
            field=models.IntegerField(
                blank=True,
                help_text="Phone number for contacting the store",
                max_length=15,
                null=True,
            ),
        ),
    ]
