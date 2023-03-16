from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from blog.forms import RegisterForms,BlogForm,AddUserForm
from blog.models import Blog
from django.conf import settings 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import Permission
# Create your views here.

#getting keyword argument from settings.py
# var = settings.CUSTOM
# demo = settings.DEBUG
# print(var)
# print(demo)

def home_page(request):
    return render(request,'main.html',{})

def create_blog(request): 
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save()
            blog.is_published = True
            blog.save()
    return render(request,'create.html', {'form': form})
    

def list_blogs(request):
    blog = Blog.objects.all()
    print(request.user)
    return render(request,'list.html', {'blog': blog})



def update_blog(request,**kwargs):
    form = BlogForm()
    msg = ''
    if request.user.is_authenticated and request.user.has_perm('blog.change_blog'):
        if request.method == 'POST':
            if id:= kwargs.get('id'):
                    obj = Blog.objects.get(id=id)
                    form = BlogForm(request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        return redirect('/demo/list')
    else:
        msg =  "You don't have the permission"
    context={'form':form,'msg':msg}
    return render(request, 'update.html' ,context)


def delete_blog(request,**kwargs):
    if request.user.is_authenticated and request.user.has_perm('blog.change_blog'):
        if pk:=kwargs.get('pk'):
            blogs = Blog.objects.get(pk=pk)
            blogs.delete()
    else:
        msg = "You don't have the permission"
    blog = Blog.objects.all()
    return render(request,'list.html', {'blog': blog,'msg':msg})

def add_blog_user(request):
    form = AddUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username, password=password)
        new_user.save()
        print(new_user.username)
    return render(request,'new_user.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
    return render(request,'login.html',{})

def user_logout(request):
    logout(request)
    return redirect("user_login")