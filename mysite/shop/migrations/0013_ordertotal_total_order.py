# Generated by Django 4.1.7 on 2023-03-27 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_ordertotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordertotal',
            name='total_order',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
