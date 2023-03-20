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
    def get(self,request):
        form = BlogForm()
        context = {'form':form}
        return render(request,'create.html',context)

    def post(self,request):
        if request.user.is_authenticated and request.user.has_perm('blog.add_blog'):
            form = BlogForm(request.POST)
            if form.is_valid():
                blog = form.save()
                blog.save()
                return redirect('list')
        return render(request,'create.html', {'form': form})

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
def update_blog(request,**kwargs):
    form = BlogForm()
    if request.user.is_authenticated and request.user.has_perm('blog.change_blog'):
        if request.method == 'POST':
            if id:= kwargs.get('id'):
                    obj = Blog.objects.get(id=id)
                    form = BlogForm(request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        return redirect('/demo/list')
    else:
        raise PermissionDenied(Exception)
    context={'form':form}
    return render(request, 'update.html', context)

#Delete existing blog
@permission_required('blog.delete_blog')
def delete_blog(request,**kwargs):
    if request.user.is_authenticated: 
        if pk:=kwargs.get('pk'):
            blogs = Blog.objects.get(pk=pk)
            blogs.delete()
    else:
       raise PermissionDenied(Exception)
    blog = Blog.objects.all()
    context = {'blog':blog}
    return render(request,'list.html',context)

#Adding new user
def add_blog_user(request):
    form = AddUserForm()
    #User Permissions
    if request.method == 'POST':
        content_type = ContentType.objects.get(app_label = 'blog', model = 'blog')
        permission = Permission.objects.get(
            codename='view_blog',
            name='Can view blog',
            content_type = content_type
        )
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username, password=password)
        new_user.user_permissions.add(permission)
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