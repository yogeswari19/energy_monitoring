# Generated by Django 4.2.1 on 2023-06-06 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0012_bookvenue_contact_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookvenue",
            name="staff_coordinator",
            field=models.CharField(default="xyz", max_length=255, null=True),
        ),
    ]
