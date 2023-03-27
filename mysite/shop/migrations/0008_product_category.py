# Generated by Django 4.1.7 on 2023-03-26 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('books', 'BOOKS'), ('toys', 'TOYS'), ('mobile', 'MOBILE'), ('nutrition', 'NUTRITION'), ('kitchen', 'KITCHEN'), ('laptop', 'LAPTOP'), ('clothes', 'CLOTHES'), ('shoes', 'SHOES')], default='mobile', max_length=20, null=True),
        ),
    ]