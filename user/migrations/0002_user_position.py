# Generated by Django 5.0.6 on 2024-06-26 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="position",
            field=models.CharField(default="Employee", max_length=100),
        ),
    ]