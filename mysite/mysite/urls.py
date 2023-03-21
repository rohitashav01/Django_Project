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
from blog.views import BlogView,BlogUpdate
from blog.views import list_blogs,add_blog_user,user_login,user_logout,home_page,publish_blog,change_password
from shop.views import add_product,product_detail,add_to_cart,remove_from_cart,add_user,add_to_wishlist

urlpatterns = [
    path('',home_page,name='home'),
    path('demo/home',BlogView.as_view(),name='class'),
    path('demo/<int:pk>/update',BlogUpdate.as_view(),name='update'),
    path('demo/<int:id>/delete',BlogUpdate.as_view(),name='delete'),
    path('demo/login',user_login,name='user_login',),
    path('admin/', admin.site.urls),
    path('demo/list',list_blogs,name='list'),
    path('demo/add',add_blog_user,name='add_user',),
    path('demo/changep',change_password,name='change_password',),
    path('demo/logout',user_logout,name='user_logout',),
    path('demo/<int:id>/publish',publish_blog,name='delete'),
    path('shop/add',add_product,name='add'),
    path('shop/details',product_detail,name='prod_detail'),
    path('shop/<int:id>',add_to_cart,name='add_cart'),
    path('remove/<int:pk>',remove_from_cart,name='remove'),
    path('shop/add_user',add_user,name='new_user'),
    path('shop/<int:pk>/wishlist',add_to_wishlist,name='wishlist')
]
