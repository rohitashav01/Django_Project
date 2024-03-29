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
from django.urls import path,include
from blog.views import BlogView,BlogUpdate
from blog.views import list_blogs,add_blog_user,user_login,user_logout,home_page,publish_blog,change_password
from shop.views import add_to_cart,remove_from_cart,add_wishlist,login_user,user_address,user_logout,cart_details,get_address,show_wishlist,past_orders,remove_from_wishlist,user_profile,edit_profile,get_all_products,UserListView
from shop import views
from blog.views import PublishedBlogView, CreateBlogView, GetBlogView, AlterBlogView, BlogViewSet, AddressViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'address', AddressViewSet, basename='address')
urlpatterns = router.urls


urlpatterns = [

    path('publishedblogs', PublishedBlogView.as_view()),
    path('blogs', CreateBlogView.as_view()),
    path('blog/<int:pk>', GetBlogView.as_view()),
    path('changeblog/<int:pk>', AlterBlogView.as_view()),


    ################################################################
    path('main-page',home_page,name='home'),
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
    # path('shop/add',add_product,name='add'),
    path('shop/<int:id>',add_to_cart,name='add_cart'),
    path('remove/<int:pk>',remove_from_cart,name='remove'),
    path('shop/<int:id>/wishlist',add_wishlist,name='wishlist'),
    path('shop/<int:id>/remove',remove_from_wishlist,name='remove-wishlist'),
    path('wishlist',show_wishlist,name='show_wishlist'),
    # path('adduser',add_user,name='adduser'),
    path('loginuser',login_user,name='loginuser'),
    path('address',user_address,name='address'),
    path('logout',user_logout,name = 'logout'),
    path('cart',cart_details,name = 'cart'),
    path('address/details',get_address,name = 'addr_details'),
    path('past-orders',past_orders,name="past-order"),


    path('listing',views.ProductListView.as_view(),name="prod_detail"),
    path('details/<int:pk>', views.ProductDetailView.as_view(), name='details'),
    path('add',views.ProductCreateView.as_view(),name='add'),
    path('new-user',views.NewUserForm.as_p,name='adduser'),
    path('profile',user_profile,name='profile'),
    path('edit-profile',edit_profile,name='edit-profile'),

    ####################################################
    path('allproducts',get_all_products),
    path('getprod/<int:pk>',views.get_product),
    path('createprod/',views.create_product),
    path('updateprod/<int:pk>',views.update_product),
    path('updateprod/<int:pk>/partial_update',views.partial_update),
    path('deleteprod/<int:pk>',views.delete_product),
    path('loginuser',views.login_user),
    path('logoutuser',views.logout_user),
    path('getaddr',views.get_address),
    path('createaddr',views.create_address),
    path('updateaddr/<int:address_id>/edit',views.update_address),
    path('partialaddr/<int:address_id>/edit',views.partial_update_address),
    path('delete_addr/<int:address_id>/delete',views.delete_address),

    path('users', UserListView.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


