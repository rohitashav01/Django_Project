from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse,Http404
from blog.forms import RegisterForms,BlogForm
from blog.models import Blog
from django.conf import settings 
# Create your views here.

#getting keyword argument from settings.py
var = settings.CUSTOM
demo = settings.DEBUG
print(var)
print(demo)

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
    return render(request,'list.html', {'blog': blog})



def update_blog(request,**kwargs):
    context = {}
    form = BlogForm()
    if id:= kwargs.get('id'):
        obj = Blog.objects.get(id=id)
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                context['form'] = form
                HttpResponseRedirect('/demo/list/')
        #context = {'form':form}
    return render(request, 'update.html' ,context)




def delete_blog(request,**kwargs):
    if pk:=kwargs.get('pk'):
        blogs = Blog.objects.get(pk=pk)
        blogs.delete()
    blog = Blog.objects.all()
    return render(request,'list.html', {'blog': blog})
