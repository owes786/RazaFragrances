# Generated by Django 5.0.1 on 2024-02-27 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_orderdetails_order_id_orderdetails_payment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='Prepaid',
            field=models.BooleanField(db_default=models.Value(False)),
        ),
    ]
