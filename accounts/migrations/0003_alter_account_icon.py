# Generated by Django 5.1.4 on 2025-01-03 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_account_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="icon",
            field=models.ImageField(
                blank=True, height_field="height", upload_to="", width_field="width"
            ),
        ),
    ]
