# Generated by Django 4.2.1 on 2023-05-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0009_alter_bookvenue_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookvenue",
            name="venue",
            field=models.CharField(default="venue name xyz", max_length=255, null=True),
        ),
    ]
