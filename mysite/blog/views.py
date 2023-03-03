from django.shortcuts import render
from django.http import HttpResponse,Http404
from blog.models import Blog
from django.utils import timezone

# Create your views here.
def addition(num1,num2):
    res = int(num1)+int(num2)
    return res
def subtract(num1,num2):
    res = int(num1)-int(num2)
    return res
def multiply(num1,num2):
    res = int(num1)*int(num2)
    return res
def divide(num1,num2):
    res = int(num1)/int(num2)
    return res

def demo(request):
    num1 = request.GET.get('num1','')
    num2 = request.GET.get('num2','')
    form = f"""
    <div id = "output">
        <form method = "GET"  >
            <input type = "text" id="num1" name = "num1" value="{num1}" />
            <input type = "text" id="num2" name = "num2" value="{num2}"/>
            <input type = "submit" name="add" value="+" />
            <input type = "submit" name="sub" value="-" />
            <input type = "submit" name="mul" value="*" />
            <input type = "submit" name="div" value="/" /> 
        </form>
    </div>
     
     """
    # scr = """
    #     <script>
    #     function formProcess(){
    #         var capture = document.forms["input"]["num1"].value + '<br>';
    #         capture += document.forms["input"]["num2"].value + '<br>';
    #         document.getElementById("output").innerHTML = capture;
    #         console.log(capture);
    #     }
    # </script>
    # """

    result = " "
    
    if  request.method  == "GET":
        
        print(request.GET)
        if 'add' in request.GET:
            result = addition(num1,num2)
        if 'sub' in request.GET:
            result = subtract(num1,num2)
        if 'mul' in request.GET:
            result = multiply(num1,num2)
        if 'div' in request.GET:
            result = divide(num1,num2)
       
    return HttpResponse(f"<html><body>{form}<h1>Output:{result}</h1></body></html>")
    


def detail(request,comment_id):
    return HttpResponse("This is the comment %s for Blog" % comment_id)

def get_data(request,b_id):
    try:
        result = Blog.objects.get(pk=b_id)
    except Blog.DoesNotExist:
        raise Http404("Blog does not exist")
    return HttpResponse(f"<html><body><h1>Blog Title: {result.title}</h1><h3>Author: {result.author}</h3><p>{result.description}</p></body></html>")



