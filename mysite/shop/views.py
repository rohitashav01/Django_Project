from django.shortcuts import render,redirect,reverse,HttpResponse,get_object_or_404
from .models import Product,ProfileUser,Address,Wishlist,Order,OrderItem,Tag
from shop.forms import ProdForm,NewUserForm,AddressForm
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


#adding a new product
def add_product(request):
    if request.method == 'POST':
        form = ProdForm(request.POST,request.FILES)
        if form.is_valid():
            prod = form.save(commit = False)
            tags = request.POST.getlist('tags')
            prod.save()
            prod.tags.set(tags)
    else:
        form = ProdForm()
    return render(request,'add.html', {'form': form})



#adding a new user
def add_user(request):
    form = NewUserForm
    if request.method == 'POST':
        form = NewUserForm(request.POST,request.FILES)
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
    return render(request,'ecom/address.html',{'form':form})


#wishlist
def add_wishlist(request,**kwargs):
    if id:=kwargs.get('id'):
        obj = Product.objects.get(id = id)
        print("===================>")
        print(obj)
        if Wishlist.objects.filter(items_id = obj).exists():
            messages.error(request,'Item already in wishlist')
        else:
            Wishlist.objects.create(items = obj,user_id = request.user.id)
        return redirect('prod_detail')

#remove from wishlist
def remove_from_wishlist(request,**kwargs):
        if id := kwargs.get('id'):
            obj = Wishlist.objects.get(id = id)
            obj.delete()
            return redirect('show_wishlist')
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


# Getting cart details
def cart_details(request):
    cart = Product.objects.all()
    return render(request,'cart.html',{'cart':cart})

#Ordered Items
def place_order(request,address_id):
    cart = request.session['cart']
    shipping_address = Address.objects.get(id = address_id)
    total_order = sum(int(p['Price']*p['Quantity']) for p in cart)
    print("================> Order Order")
    var = Order.objects.create(user_id=request.user.id, address=shipping_address, total_order=total_order)
    order_items(request,var.pk)
    messages.success(request,'Order placed successfully')
    
def order_items(request,o_id):
    cart = request.session['cart']
    print("================> Order Item")
    for i in cart:
        total = int(i['Price']*i['Quantity'])
        OrderItem.objects.create(product_id=i['ID'],total=total,order_id=o_id)
  
#Selecting address during checkout  
def get_address(request):
    cart = request.session['cart']
    total = sum(int(p['Price']) * p['Quantity']  for  p in cart)
    data = Address.objects.filter(user_id=request.user.id)
    if request.method == 'POST':
        if 'data' in request.POST:
            data = request.POST['data']
            print(data)
            place_order(request,data)
            return redirect('addr_details')
        else:
            messages.error(request,'Please select an address')
    return render(request,'ecom/checkout.html',{'data':data,'total':total})


#Getting Past Orders
def past_orders(request):
    obj = Order.objects.filter(user_id = request.user.id)
    return render(request,'ecom/past_orders.html',{'obj':obj})


#get related products
def get_related_products(product):
    print(product.tags.tags__id)
    related_products = Product.objects.filter()
    return related_products.exclude(id=product.id)

#get details of the product
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = get_related_products(product)
    context = {
        'product':product,
        'related_products':related_products
    }
    return render(request,'ecom/product_detail.html',context)

#Pagination
def listing(request):
    prod_list = Product.objects.all()
    paginator = Paginator(prod_list, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'details.html', {'prod': page_obj})

#user profile
def user_profile(request):
    return render(request,'ecom/userprofile.html',{})

def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        u = ProfileUser.objects.get(username=username)
        u.set_password(new_password)    
        u.save()
        messages.success(request,'Password Changed')
        return redirect('prod_detail')
    return render(request,'ecom/editprofile.html',{})