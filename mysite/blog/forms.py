from django import forms
from blog.models import Blog

class RegisterForms(forms.Form):
    num1 = forms.CharField()
    num2 = forms.CharField()

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','author','description','is_published','published_on']

class AddUserForm(forms.Form):
    username = forms.CharField(max_length=20,label='Enter Name of User')
    password = forms.CharField(widget=forms.PasswordInput)


