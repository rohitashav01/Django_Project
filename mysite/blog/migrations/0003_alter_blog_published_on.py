# Generated by Django 4.1.7 on 2023-03-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blog_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='published_on',
            field=models.DateField(),
        ),
    ]
