# Generated by Django 4.1.7 on 2023-03-23 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
