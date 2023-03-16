from django.shortcuts import render,redirect,reverse,HttpResponseRedirect
from blog.forms import RegisterForms,BlogForm,AddUserForm
from blog.models import Blog
from django.conf import settings 
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.contenttypes.models import ContentType
# Create your views here.

#getting keyword argument from settings.py
# var = settings.CUSTOM
# demo = settings.DEBUG
# print(var)
# print(demo)

#User Permissions

author_group, created = Group.objects.get_or_create(name="Author")
admin_group, created = Group.objects.get_or_create(name="Admin")
publisher_group, created = Group.objects.get_or_create(name="Publisher")


def home_page(request):
    return render(request,'main.html',{})

def create_blog(request): 
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save()
            blog.save()
            return redirect('list')
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
    context = {'blog':blog,'msg':msg}
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

#User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
    return render(request,'login.html',{})

#User Logout
def user_logout(request):
    logout(request)
    return redirect("home")

#Publish Blog
def publish_blog(request,**kwargs):
    # import pdb;pdb.set_trace()
    print(request.method)
    if request.method == 'GET':
        if id:= kwargs.get('id'):
            blog = Blog.objects.get(id=id)
            blog.is_published = True
            blog.save()
    return render(request,'published.html',{'blog':blog})