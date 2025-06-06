# Generated by Django 5.1.5 on 2025-03-18 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0024_alter_saleproducts_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleproducts',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='catalog.product'),
        ),
    ]
