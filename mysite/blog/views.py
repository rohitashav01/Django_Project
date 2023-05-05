from django.shortcuts import render,redirect,reverse,HttpResponse
from django.http import Http404
from blog.forms import RegisterForms,BlogForm,AddUserForm
from blog.models import Blog
from django.conf import settings 
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.views import View

#getting keyword argument from settings.py
# var = settings.CUSTOM
# demo = settings.DEBUG

class BlogView(View):
    form = BlogForm()
    def get(self,request):
        form = BlogForm(request.POST)
        context = {'form':form}
        return render(request,'create.html',context)

    def post(self,request):
        if request.user.is_authenticated and request.user.has_perm('blog.add_blog'):
            form = BlogForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('list')
        return render(request,'create.html', {'form': form})
    
class BlogUpdate(View):
    form = BlogForm()
    def get(self,request,**kwargs):
        form = BlogForm(request.POST)
        if id:=kwargs.get('id'):
            obj = Blog.objects.get(id=id)
            form = BlogForm(request.POST,instance = obj)
        context = {'form':form}
        return render(request,'update.html',context)
    
    def put(self,request,**kwargs):
        if request.user.is_authenticated and request.user.has_perm('blog.change_blog'):
                if id:= kwargs.get('id'):
                        obj = Blog.objects.get(id=id)
                        form = BlogForm(request.PUT, instance = obj)
                        if form.is_valid():
                            form.save()
                        return redirect('list')
        else:
            raise PermissionDenied(Exception)
        return render(request, 'update.html', {'form':form})
    

    # def get(self,request,**kwargs):
    #     if id:=kwargs.get('id'):
    #         demo = Blog.objects.get(id=id)
    #     return render(request,'list.html',{'demo':demo})
    
    def delete(self,request):
        print("========================>")
        print("yes")
        if request.user.is_authenticated and request.user.has_perm('blog.delete_blog'): 
            blogs = Blog.objects.get(pk=id)
            blogs.delete()
        else:
            raise PermissionDenied(Exception)
        blog = Blog.objects.all()
        context = {'blog':blog}
        return render(request,'list.html',context)

    # def create_blog(request): 
    #     if request.user.is_authenticated and request.user.has_perm('blog.add_blog'):
    #         if request.method == 'POST':
    #             form = BlogForm(request.POST)
    #             if form.is_valid():
    #                 blog = form.save()
    #                 blog.save()
    #                 return redirect('list')
    #     else:
    #        raise PermissionDenied(Exception)
    #     return render(request,'create.html', {'form': form})



#User Permissions
author_group, created = Group.objects.get_or_create(name="Author")
admin_group, created = Group.objects.get_or_create(name="Admin")
publisher_group, created = Group.objects.get_or_create(name="Publisher")

#Home Page
def home_page(request):
    return render(request,'main.html',{})

#Add a new blog
def list_blogs(request):
    blog = Blog.objects.all()
    return render(request,'list.html', {'blog': blog})

#Update Blog
# def update_blog(request,**kwargs):
#     form = BlogForm()
#     if request.user.is_authenticated and request.user.has_perm('blog.change_blog'):
#         if request.method == 'POST':
#             if id:= kwargs.get('id'):
#                     obj = Blog.objects.get(id=id)
#                     form = BlogForm(request.POST, instance=obj)
#                     if form.is_valid():
#                         form.save()
#                         return redirect('/demo/list')
#     else:
#         raise PermissionDenied(Exception)
#     context={'form':form}
#     return render(request, 'update.html', context)

#Delete existing blog
# @permission_required('blog.delete_blog')
# def delete_blog(request,**kwargs):
#     if request.user.is_authenticated: 
#         if pk:=kwargs.get('pk'):
#             blogs = Blog.objects.get(pk=pk)
#             blogs.delete()
#     else:
#        raise PermissionDenied(Exception)
#     blog = Blog.objects.all()
#     context = {'blog':blog}
#     return render(request,'list.html',context)

#Adding new user
def add_blog_user(request):
    form = AddUserForm()
    #User Permissions
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username, password=password)
        new_user.save()
        return redirect('home')
    return render(request,'new_user.html',{'form':form})

def change_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        u = User.objects.get(username=username)
        u.set_password(new_password)    
        u.save()
        return redirect('home')
    return render(request,'profile.html',{})

#User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("user does not exist")
    return render(request,'login.html',{})

#User Logout
def user_logout(request):
    logout(request)
    return redirect("home")

#Publish Blog
def publish_blog(request,**kwargs):
    # import pdb;pdb.set_trace()
    if request.user.is_authenticated and request.user.has_perm('blog.can_publish'):
        if request.method == 'GET':
            if id:= kwargs.get('id'):
                blogs = Blog.objects.get(id=id)
                blogs.is_published = True
                blogs.save()
    else:
        raise PermissionDenied(Exception)
    return render(request,'published.html',{'blogs':blogs})

############################################# Generic Views ############################################################

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.serializers import ModelSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from  django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter 

###----From Shop app ---- ####
from shop.models import ProfileUser, Address



class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class PublishedBlogView(ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

class CreateBlogView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        response.data = {"message":"Blog Created Successfully"}
        return response

class GetBlogView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"title":serializer.data['title']})


class AlterBlogView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def update(self, request, *args, **kwargs):
        serializer = super().update(request, *args, **kwargs)
        serializer.data = {"message": "Blog Updated Successfully"}
        return serializer
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {"message":"Blog Deleted Successfully"}
        return response

#################################### Viewsets ########################################

#Filtering Using Class
class BlogFilterSet(FilterSet):
    title = CharFilter(lookup_expr='contains')
    class Meta:
        model = Blog
        fields = ['title','is_published']
        

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilterSet
    
    def create(self, request, *args, **kwargs):
        instance = super().create(request, *args, **kwargs)
        instance.data = {"message":"Blog Created Successfully"}
        return instance
    
    def update(self, request, *args, **kwargs):
        instance = super().update(request, *args, **kwargs)
        instance.data = {"message":"Blog Updated Successfully"}
        return instance
   
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.status_code = status.HTTP_202_ACCEPTED
        response.data = {"msg":"Deleted Successfully"}
        return response
    

############---- Filtering Foreign Key----####################
class AddressSerilazer(ModelSerializer):
    class Meta:
        model = Address
        fields ='__all__'

class AddressFilterSet(FilterSet):
    user_id = CharFilter(lookup_expr='exact')
    class Meta:
        model = Address
        fields = ['user_id']
        
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerilazer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AddressFilterSet
    
    