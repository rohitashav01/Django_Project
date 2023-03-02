from django.shortcuts import render
from django.http import HttpResponse



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

    form = """
    <div id = "output">
        <form method = "GET" onsubmit = "return false" >
            <input type = "text" name = "num1"  />
            <input type = "text" name = "num2" />
            <input type = "submit" name="add" id ="demo" value="+" onclick="formProcess()"/>
            <input type = "submit" name="sub" value="-" onclick="formProcess()"/>
            <input type = "submit" name="mul" value="*" onclick="formProcess()"/>
            <input type = "submit" name="div" value="/" onclick="formProcess()"/> 
        </form>
    </div>
     
    """
    scr = """
        function formProcess(){
            
            var capture = document.forms["input"]["demo"].value;
            capture += document.forms["input"]["num2"].value;
            document.getElementById("output").innerHTML = capture;
            console.log(capture);
        }
    """

    result = " "
    
    if  request.method  == "GET":
        num1 = request.GET.get('num1')
        num2 = request.GET.get('num2')
        print(request.GET)
        if 'add' in request.GET:
            result = addition(num1,num2)
        if 'sub' in request.GET:
            result = subtract(num1,num2)
        if 'mul' in request.GET:
            result = multiply(num1,num2)
        if 'div' in request.GET:
            result = divide(num1,num2)
       
    return HttpResponse(f"<html><body>{form}<h1>Output:{result}</h1><script>{scr}</script></body></html>")
    


