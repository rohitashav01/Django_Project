from django.db import models

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=150)
    description = models.TextField()
    is_published = models.BooleanField()
    published_on = models.DateTimeField()


