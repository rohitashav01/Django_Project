from django.shortcuts import render,redirect
from blog.forms import RegisterForms,BlogForm
from blog.models import Blog
# Create your views here.

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
    error_msg = ""
    form = BlogForm()
    if request.method == 'POST':
        if id:= kwargs.get('id'):
            try:
                obj = Blog.objects.get(id=id)
                form = BlogForm(request.POST or None, instance=obj)
                if form.is_valid():
                    demo = form.save()
                    demo.is_published = True
                    demo.save()
                    return redirect('/demo/list')
            except Exception as e:
                error_msg = "Blog does not exist"

    context = {'form':form,'error_msg':error_msg}
    return render(request, 'update.html',context)


def delete_blog(request,**kwargs):
    if pk:=kwargs.get('pk'):
        blogs = Blog.objects.get(pk=pk)
        blogs.delete()
    blog = Blog.objects.all()
    return render(request,'list.html', {'blog': blog})
