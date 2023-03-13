from django.db import models
from django.conf import settings
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    quantity = models.IntegerField()
  
class Cart(models.Model):
    prod = models.ForeignKey(Product,on_delete=models.CASCADE)
    prod_price = models.IntegerField(null=False)
    prod_qty = models.IntegerField(null = False)