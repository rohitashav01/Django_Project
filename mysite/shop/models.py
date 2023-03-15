from django.db import models
from django.conf import settings
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    quantity = models.IntegerField()
  

    
