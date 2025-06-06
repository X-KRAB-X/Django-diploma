# Generated by Django 5.1.5 on 2025-02-14 09:23

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_tag_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='catalog.product'),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rate',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
