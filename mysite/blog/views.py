from django.shortcuts import render
from django.http import HttpResponse,Http404
from blog.forms import RegisterForms,BlogForm

# Create your views here.


def demo(request): 
    # num1 = request.GET.get('num1','')
    # num2 = request.GET.get('num2','')

    # def addition(num1,num2):
    #     res = int(num1)+int(num2)
    #     return res
    # def subtract(num1,num2):
    #     res = int(num1)-int(num2)
    #     return res
    # def multiply(num1,num2):
    #     res = int(num1)*int(num2)
    #     return res
    # def divide(num1,num2):
    #     res = int(num1)/int(num2)
    #     return res
    
    
    # result = ''
    # if  request.method  == "GET":
    #     if 'add' in request.GET:
    #         result = addition(num1,num2)
    #     if 'sub' in request.GET:
    #         result = subtract(num1,num2)
    #     if 'mul' in request.GET:
    #         result = multiply(num1,num2)
    #     if 'div' in request.GET:
    #         result = divide(num1,num2)
    
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save()
            blog.is_published = True
            blog.save()
    return render(request,'index.html', {'form': form})
    


# def detail(request,comment_id):
#     return HttpResponse("This is the comment %s for Blog" % comment_id)

# def get_data(request,b_id):
#     try:
#         result = Blog.objects.get(pk=b_id)
#     except Blog.DoesNotExist:
#         raise Http404("Blog does not exist")
#     return HttpResponse(f"<html><body><h1>Blog Title: {result.title}</h1><h3>Author: {result.author}</h3><p>{result.description}</p></body></html>")



