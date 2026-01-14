from django import forms
from .models import Tovar

class PostForm(forms.ModelForm):
    class Meta:
        model = Tovar

        fields = ['title', 'text', 'image', 'author']
