# Generated by Django 5.1.4 on 2025-01-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0007_category_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="date",
        ),
        migrations.AddField(
            model_name="transaction",
            name="date",
            field=models.DateField(db_default="2021-12-31"),
        ),
    ]
