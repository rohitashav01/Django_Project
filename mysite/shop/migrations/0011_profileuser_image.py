# Generated by Django 4.1.7 on 2023-03-27 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
