
from django import forms
from shop.models import Product,ProfileUser,Address
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput,Select,CheckboxInput,ImageField

class ProdForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','quantity','category','image']
    
class NewUserForm(forms.ModelForm):
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    class Meta:
        model = ProfileUser
        fields = ['username','age','email','password','image']
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Name'
                }),
            'age': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'age'
                }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'email'
            }),
            'password': PasswordInput(attrs={
                'class': "form-control",
                'placeholder': 'Password'
                }),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address','city','state','zipcode','country']
        widgets = {
            'address': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Address'
                }),
            'city': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'City'
                }),
            'state': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'State'
            }),
            'zipcode': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Zip'
                }),
        }


