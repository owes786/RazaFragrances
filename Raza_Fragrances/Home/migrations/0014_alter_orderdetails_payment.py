# Generated by Django 5.0.1 on 2024-03-13 05:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0013_orderdetails_payment_alter_orderdetails_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='Payment',
            field=models.ForeignKey(db_default=models.Value('COD'), null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.payment'),
        ),
    ]
