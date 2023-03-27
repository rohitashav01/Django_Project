from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

CATEGORY_CHOICES = [
    ('books','BOOKS'),
    ('toys','TOYS'),
    ('mobile','MOBILE'),
    ('nutrition','NUTRITION'),
    ('kitchen','KITCHEN'),
    ('laptop','LAPTOP'),
    ('clothes','CLOTHES'),
    ('shoes','SHOES')

]

class Product(models.Model):
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default = 'mobile',blank=True, null=True)
    image = models.ImageField(upload_to='images/')

class ProfileUser(AbstractUser):
    username = models.CharField(max_length=20)
    age = models.IntegerField(blank = True,null=True)
    email = models.EmailField(max_length=254, unique=True)
    image = models.ImageField(upload_to='images/',null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

class Address(models.Model):
    user = models.ForeignKey(ProfileUser,on_delete = models.CASCADE)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60, default="Chandigarh")
    state = models.CharField(max_length=30, default="Punjab")
    zipcode = models.CharField(max_length=6, default="176302")
    country = models.CharField(max_length=50, default = 'India')


class Wishlist(models.Model):
    items = models.ForeignKey(Product,on_delete = models.CASCADE)
    user = models.ForeignKey(ProfileUser,on_delete = models.CASCADE)


class Order(models.Model):  
    user = models.ForeignKey(ProfileUser,on_delete=models.CASCADE)
    total_order = models.CharField(max_length=1000,null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    total = models.CharField(max_length=200)
    ordered_at = models.DateTimeField(auto_now=True)

