"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog.views import create_blog,list_blogs,update_blog,delete_blog
from shop.views import add_product,product_detail,add_to_cart
urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/create',create_blog,name='create'),
    path('demo/list',list_blogs,name='list'),
    path('demo/<int:id>/update',update_blog,name='update'),
    path('demo/<int:pk>/delete',delete_blog,name='delete'),
    path('shop/add',add_product,name='add'),
    path('shop/details',product_detail,name='detail'),
    path('shop/<int:id>/cart',add_to_cart,name='add_cart')
]
