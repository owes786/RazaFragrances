# Generated by Django 5.0.1 on 2024-03-13 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0016_alter_orderdetails_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='Payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.payment'),
        ),
    ]
