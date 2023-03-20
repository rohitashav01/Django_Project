from shop.models import Product
from django.shortcuts import render,redirect,reverse,HttpResponse


def add_to_cart_helper(request,**kwargs):
    if id := kwargs.get('id'):
        data = Product.objects.get(id = id)
        cart = request.session.get('cart',[])
        cart_items = {'ID':data.pk,'Name':data.name,'Price':data.price,'Quantity':1}
        if cart != []:
            for i in cart:
                print(i)
                print(i['ID'])
                print(data.pk)
                if i['ID'] == data.pk:
                    print(i['ID'])
                    i['Quantity'] += 1
                    print('this is from if')
                else:
                    print('this is from else')
                    cart.append(cart_items)       
        else:
            data = Product.objects.get(id = id)
            cart.append(cart_items)
        request.session['cart'] = cart
    return request.session['cart']


def remove_from_cart_helper(request,**kwargs):
    if id:=kwargs.get('pk'):
        data = Product.objects.get(id=id)
        for item in request.session['cart']:
            #import pdb;pdb.set_trace()
            if item['ID'] == data.pk:
                cart = request.session.get('cart',[])
                cart.remove(item)
                request.session['cart'] = cart
            else:
                print('Not found')
    return request.session['cart']