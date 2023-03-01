from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def demo(request):
    return HttpResponse("hello this is from the views file")

def Form(request):
    form = """
    <form action = "" method = "GET">
        <input type = "text" name = "num1"/>
        <input type = "text" name = "num2"/>
        <input type = "button" value = "+"/>
        <input type = "button" value = "-"/>
        <input type = "button" value = "*"/>
        <input type = "button" value = "/"/>
        <a href = "/addition">Add</a>
    </form>
    <a href = "/calculator"> Another Page </a>
    
    """
    return HttpResponse(f"<html><body>{form}</body></html>")

def calcul(request):
    return HttpResponse("This is the calculator")

