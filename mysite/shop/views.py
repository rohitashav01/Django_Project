from django.shortcuts import render,redirect,reverse
from .models import Product,Cart
from shop.forms import ProdForm,AddUser
from django.contrib.auth.models import User
from django.contrib import messages

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


    if id := kwargs.get('id'):

        #from database
        data = Product.objects.get(id = id)

        cart_data = Cart.objects.create(prod_id = id)
        cart_data.save()

        #from session
        cart_items = [{'Name':data.name,'Price':data.price}]
        cart = request.session.get('cart',[])
        cart.append(cart_items)
        request.session['cart'] = cart
        

          
        #cook = request.META.get('HTTP_COOKIE')
    data = Cart.objects.all()
    return render(request,'cart.html',{'data':data})



def remove_from_cart(request,**kwargs):
    if pk:=kwargs.get('pk'):
        del_data = Cart.objects.get(pk = pk)
        del_data.delete()
    data = Cart.objects.all()
    return render(request,'cart.html', {'data':data})

