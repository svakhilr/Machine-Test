# Generated by Django 5.0.4 on 2024-05-01 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_purchaseorder_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='rating_point',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]