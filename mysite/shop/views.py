from django.shortcuts import render,redirect,reverse,HttpResponse
from .models import Product,ProfileUser,Address,Wishlist,Order
from shop.forms import ProdForm,NewUserForm,AddressForm,ShippingAddressSelectForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from mysite.core.helper import add_to_cart_helper,remove_from_cart_helper,add_to_wishlist_helper,remove_from_wishlist_helper
from django.core.paginator import Paginator
# Create your views here.

# def add_user(request):
#     form = AddUser()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         new_user = User.objects.create_user(username, password)
#         new_user.save()
#     return render(request,'new_user.html',{'form':form})


#adding a new user
def add_product(request):
    form = ProdForm
    if request.method == 'POST':
        form = ProdForm(request.POST)
        if form.is_valid():
            prod = form.save()
            prod.save()
    return render(request,'add.html', {'form': form})

#adding a new user
def add_user(request):
    form = NewUserForm
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prod_detail')
    return render(request,'ecom/adduser.html',{'form':form})


#login User
def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Login Successfully')
        else:
            messages.error(request,'Invalid Credentials or user does not exist')
    return render(request,'ecom/login_user.html',{})

#User Logout
def user_logout(request):
    cart = request.session.get('cart',[])
    if cart != []:
        del request.session['cart']
        logout(request)
    else:
        logout(request)
    return redirect("prod_detail")

#Add User Address
def user_address(request):
    form = AddressForm
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user_id = request.user.id
            print(instance.user_id)
            instance.save()
            return redirect('prod_detail')
    else:
        obj = Address.objects.get(user_id = request.user.id)
    return render(request,'ecom/address.html',{'form':form,'obj':obj})

def get_address(request):
    cart = request.session['cart']
    total = sum(int(p['Price']) * p['Quantity']  for  p in cart)
    data = Address.objects.filter(user_id = request.user.id)
    return render(request,'ecom/checkout.html',{'data':data,'total':total})

#wishlist
def add_wishlist(request,**kwargs):
    if id:=kwargs.get('id'):
        obj = Product.objects.get(id = id)
        Wishlist.objects.create(items = obj,user_id = request.user.id)
        return redirect('prod_detail')

#show wishlist
def show_wishlist(request):
    data = Wishlist.objects.filter(user_id = request.user.id)
    return render(request,'ecom/wishlist.html',{'data':data})


#helper functions
def add_to_cart(request,**kwargs):
    cart = add_to_cart_helper(request,**kwargs)
    print(cart)
    return render(request,'cart.html',{'cart':cart})

def remove_from_cart(request,**kwargs):
    var = remove_from_cart_helper(request,**kwargs)
    print(var)
    return render(request,'cart.html',{'var':var})


#cart details
def cart_details(request):
    cart = Product.objects.all()
    return render(request,'cart.html',{'cart':cart})


def place_order(request):
    cart = request.session['cart']
    # shipping_address = Address.objects.filter(user_id = request.user.id)
    shipping_address_select_form = ShippingAddressSelectForm(user = request.user)
    if request.method == 'POST':
        shipping_address = shipping_address_select_form.cleaned_data['shipping_address']
    print(shipping_address)
    product = request.session.get('cart',[])
    for p in cart:
        sum = int(p['Price']*p['Quantity'])
        order = Order.objects.create(user_id = request.user.id, address = shipping_address,total = sum,product_id = p['ID'])
        messages.success(request,'Order placed successfully')
    del cart
    return render(request,'ecom/checkout.html',{'shipping_address_select_form':shipping_address_select_form})    

def past_orders(request):
    obj = Order.objects.filter(user_id = request.user.id)
    return render(request,'ecom/past_orders.html',{'obj':obj})

#Pagination
def listing(request):
    prod_list = Product.objects.all()
    paginator = Paginator(prod_list, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'details.html', {'prod': page_obj})