# Generated by Django 4.1.7 on 2023-03-09 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remove_blog_published_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='published_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
