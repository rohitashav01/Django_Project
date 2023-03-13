
from django import forms
from shop.models import Product

class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','quantity']

