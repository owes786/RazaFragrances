# Generated by Django 4.2.7 on 2023-12-12 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_cart_customer_details_orderdetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='List_Product',
            new_name='Product',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='list_Product',
            new_name='Product',
        ),
    ]
