from django.contrib import admin
from .models import Product,ProfileUser,Address,Wishlist,Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','quantity','category','image']

admin.site.register(Product,ProductAdmin)
admin.site.register(ProfileUser)
admin.site.register(Address)
admin.site.register(Wishlist)
admin.site.register(Order)