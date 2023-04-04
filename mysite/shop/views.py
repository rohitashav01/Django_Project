from django.shortcuts import render,redirect,reverse,HttpResponse,get_object_or_404
from .models import Product,ProfileUser,Address,Wishlist,Order,OrderItem,Tag
from shop.forms import ProdForm,NewUserForm,AddressForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from mysite.core.helper import add_to_cart_helper,remove_from_cart_helper,add_to_wishlist_helper,remove_from_wishlist_helper
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
###########################################


from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.serializers import ModelSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .permissions import UserPermission
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
# Create your views here.

# def add_user(request):
#     form = AddUser()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         new_user = User.objects.create_user(username, password)
#         new_user.save()
#     return render(request,'new_user.html',{'form':form})

class ProductListView(ListView):
    model = Product
    paginate_by = 8
    template_name = 'details.html'
    context_object_name = 'product_list'

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['count'] = Product.objects.count()
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'ecom/product_detail.html'
    context_object_name = 'product'
    

class ProductCreateView(CreateView):
    model = Product
    template_name = 'add.html'
    fields = '__all__'
    success_url="/success"

class UserFormView(FormView):
    form_class = NewUserForm
    template_name='ecom/adduser.html'
    success_url = '/prod_detail'

    def form_valid(self, form):
        return super().form_valid(form)
    
#adding a new product\
# def add_product(request):
#     if request.method == 'POST':
#         form = ProdForm(request.POST,request.FILES)
#         if form.is_valid():
#             prod = form.save(commit = False)
#             tags = request.POST.getlist('tags')
#             prod.save()
#             prod.tags.set(tags)
#     else:
#         form = ProdForm()
#     return render(request,'add.html', {'form': form})
# #get related products
# def get_related_products(product):
#     print(product.tags.tags__id)
#     related_products = Product.objects.filter()
#     return related_products.exclude(id=product.id)

# #get details of the product
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     related_products = get_related_products(product)
#     context = {
#         'product':product,
#         'related_products':related_products
#     }
#     return render(request,'ecom/product_detail.html',context)

# #Pagination
# def listing(request):
#     prod_list = Product.objects.all()
#     paginator = Paginator(prod_list, 12) 
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'details.html', {'prod': page_obj})





# #adding a new user
# def add_user(request):
#     form = NewUserForm
#     if request.method == 'POST':
#         form = NewUserForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('prod_detail')
#     return render(request,'ecom/adduser.html',{'form':form})


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
    var = Order.objects.create(user_id=request.user.id, address=shipping_address, total_order=total_order)
    order_items(request,var.pk)
    messages.success(request,'Order placed successfully')
    
def order_items(request,o_id):
    cart = request.session['cart']
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



################################################################API###############################################################
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

@api_view()
def get_all_products(request):
    products = Product.objects.all()
    return Response({"products":ProductSerializer(products, many=True).data})

#crud for products

#get product
@api_view(http_method_names=('get',))
def get_product(request,pk):
    prod = Product.objects.get(id=pk)
    return Response({"product":ProductSerializer(prod).data})

#create product
@api_view(http_method_names=('post',))
@permission_classes([IsAuthenticated])
def create_product(request):
    try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            prod = Product.objects.all().last()
            return Response({"new_product":ProductSerializer(prod).data})
    except:
        raise exceptions.status.HTTP_403_FORBIDDEN


#update
@api_view(http_method_names=('put',))
@permission_classes([IsAdminUser])
def update_product(request,pk):
    prod = Product.objects.get(id=pk)
    serializer = ProductSerializer(prod, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"updated_product":ProductSerializer(prod).data})

#partial_update
@api_view(http_method_names=('patch',))
@permission_classes([IsAdminUser])
def partial_update(request,pk):
    prod = Product.objects.get(id=pk)   
    serializer = ProductSerializer(prod, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"updated_product":ProductSerializer(prod).data})

#delete
@api_view(http_method_names=('delete',))
@permission_classes([IsAdminUser])
def delete_product(request,pk):
    prod = Product.objects.get(id=pk)   
    prod.delete()
    return Response({"message":"product_deleted"})




###################################################
#crud for address
class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = "__all__"


#get_address
@csrf_exempt
@api_view(http_method_names=('post',))
def login_user(request):
    email = request.data.get('email')
    user_email = ProfileUser.objects.get(email=email)
    serializer = ProfileSerializer(user_email)
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        try:
            login(request, user)
            var = Token.objects.create(user=user_email)
            return Response({"Status":"Login Successful","Message":serializer.data,"Token":var.key},status=status.HTTP_200_OK)
        
        except ProfileUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Credentials', status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=('post',))
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({"message":"User logged out!!!!!"},status.HTTP_202_ACCEPTED)
    except:
        return Response({"message":"No user logged in"})

@api_view(http_method_names=('get',))
@permission_classes([UserPermission])
def get_address(request):
    address = Address.objects.filter(user_id=request.user.id)
    return Response({"address":AddressSerializer(address,many=True).data})

#create address
@api_view(http_method_names=('post',))
@permission_classes([IsAuthenticated])
def create_address(request):
    request.data["user"]=request.user.id
    serializer = AddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    new_address = Address.objects.filter(user=request.user).last()
    return Response({"new_address":AddressSerializer(new_address).data})

#update address
@api_view(http_method_names=('put',))
@permission_classes([IsAuthenticated])
def update_address(request,address_id):
    request.data["user"]=request.user.id
    address = get_object_or_404(Address, user_id=request.data["user"], id=address_id) 
    serializer = AddressSerializer(address, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"updated_address":AddressSerializer(address).data})


#partial update
@api_view(http_method_names=('patch',))
@permission_classes([IsAuthenticated])
def partial_update_address(request,address_id):
    request.data["user"]=request.user.id
    address = get_object_or_404(Address, user_id=request.user.id, id=address_id)
    serializer = AddressSerializer(address, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"changed_address":AddressSerializer(address).data})

#delete address
@api_view(http_method_names=('delete',))
def delete_address(request,address_id):
    request.data["user"]=request.user.id
    address = get_object_or_404(Address, user_id=request.user.id, id=address_id)
    address.delete()
    return Response({"message":"Address Deleted"})


####################################################################################


class UserSerializer(ModelSerializer):
    f_name = serializers.SerializerMethodField()
    def get_f_name(self, name):
        fn = name.first_name + " " + name.last_name
        return fn
    
    class Meta:
        model = ProfileUser
        fields = ['first_name', 'last_name', 'f_name']

class UserListView(ListAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = UserSerializer   
