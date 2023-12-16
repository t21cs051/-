# Generated by Django 4.1 on 2023-12-16 06:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("master", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="powersystem",
            name="max_current",
            field=models.FloatField(
                default=0.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(100.0),
                ],
            ),
        ),
    ]
