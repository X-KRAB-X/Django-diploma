# Generated by Django 5.1.5 on 2025-03-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_order_ispayed'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='isDeleted',
            field=models.BooleanField(default=False),
        ),
    ]
