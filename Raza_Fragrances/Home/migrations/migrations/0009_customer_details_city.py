# Generated by Django 5.0 on 2023-12-18 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_alter_orderdetails_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_details',
            name='City',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
