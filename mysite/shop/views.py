from django.shortcuts import render,redirect,reverse,HttpResponse
from .models import Product
from shop.forms import ProdForm,AddUser
from django.contrib.auth.models import User
from django.contrib import messages
from mysite.core.helper import add_to_cart_helper,remove_from_cart_helper 
# Create your views here.

def add_user(request):
    form = AddUser()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        new_user = User.objects.create_user(username, password)
        new_user.save()
    return render(request,'new_user.html',{'form':form})

def add_product(request):
    form = ProdForm
    if request.method == 'POST':
        form = ProdForm(request.POST)
        if form.is_valid():
            prod = form.save()
            prod.save()
    return render(request,'add.html', {'form': form})

def product_detail(request):
    prod = Product.objects.all()
    return render(request,'details.html',{'prod':prod})


def add_to_cart(request,**kwargs):
        cart = add_to_cart_helper(request,**kwargs)
        print(cart)

        return render(request,'cart.html',{'cart':cart})

def remove_from_cart(request,**kwargs):
      var = remove_from_cart_helper(request,**kwargs)
      print(var)
      return render(request,'cart.html',{'var':var})
