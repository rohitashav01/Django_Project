from django.contrib import admin
from .models import Product,ProfileUser,Address,Wishlist,Order,Tag

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','quantity','category','image']

class TagAdmin(admin.ModelAdmin):
    list_display = ['tagname']
admin.site.register(Product,ProductAdmin)
admin.site.register(ProfileUser)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(Tag,TagAdmin)