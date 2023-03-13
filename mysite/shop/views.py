from django.shortcuts import render
from .models import Product
from shop.forms import ProdForm

# Create your views here.
def add_product(request):
    form = ProdForm
    if request.method == 'POST':
        form = ProdForm(request.POST)
        if form.is_valid():
            prod = form.save()
            prod.save()
    return render(request,'add.html', {'form': form})

def product_detail(request):
    prod = Product.objects.all()
    return render(request,'details.html',{'prod':prod})

def add_to_cart(request,**kwargs):

    if id := kwargs.get('id'):
        data = Product.objects.get(id = id)
        context['data']=data

    context = {}   
    return render(request,'cart.html',context)