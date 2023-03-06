from django import forms
from blog.models import Blog

class RegisterForms(forms.Form):
    num1 = forms.CharField()
    num2 = forms.CharField()

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','author','description','published_on']