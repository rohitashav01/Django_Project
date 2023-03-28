from shop.models import Product
from django.shortcuts import render,redirect,reverse,HttpResponse


def add_to_cart_helper(request,**kwargs):
    if id := kwargs.get('id'):
        data = Product.objects.get(id = id)
        cart = request.session.get('cart',[])
        if cart == []:
            cart_items = {'ID':data.pk,'Name':data.name,'Price':data.price,'Quantity':1,'Image':data.image.url}
            cart.append(cart_items)
        else:
            for i in cart:
                if i['Id'] == data.pk:
                    i['quantity'] += 1
                    break

            cart_items = {'ID':data.pk,'Name':data.name,'Price':data.price,'Quantity':1,'Image':data.image.url}
            cart.append(cart_items)
            
        request.session['cart'] = cart
    return request.session['cart']


def remove_from_cart_helper(request,**kwargs):
    if id:=kwargs.get('pk'):
        data = Product.objects.get(id=id)
        for item in request.session['cart']:
            if item['ID'] == data.pk:
                cart = request.session.get('cart',[])
                cart.remove(item)
                request.session['cart'] = cart
            else:
                print('Not found')
    return request.session['cart']



def add_to_wishlist_helper(request,**kwargs):
    if id := kwargs.get('id'):
        data = Product.objects.get(id=id)
        print(data.pk)
        wishlist = request.session.get('wishlist',[])
        wish_items = {'ID':data.pk,'Name':data.name,'Price':data.price,'Quantity':data.quantity}
        wishlist.append(wish_items)
        request.session['wishlist'] = wishlist
    return request.session['wishlist']


def remove_from_wishlist_helper(request,**kwargs):
    if id:=kwargs.get('pk'):
        data = Product.objects.get(id=id)
        for item in request.session['wishlist']:
            if item['ID'] == data.pk:
                wishlist = request.session.get('wishlist',[])
                del wishlist
                request.session['wishlist'] = wishlist
            else:
                print('Not found')
    return request.session['wishlist'] 