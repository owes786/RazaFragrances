# Generated by Django 5.0.1 on 2024-03-15 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0019_alter_orderdetails_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='Razorpay_Order_id',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='Razorpay_Payment_id',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='Razorpay_signature',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
