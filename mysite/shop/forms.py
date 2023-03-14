
from django import forms
from shop.models import Product

class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','quantity']

class AddUser(forms.Form):
    username = forms.CharField(max_length=20,label='Enter Name of User')
    password = forms.CharField(widget=forms.PasswordInput)

    