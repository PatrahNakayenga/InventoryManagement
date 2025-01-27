from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import inventoryItem, Category

class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']





class InventoryItemForm(forms.ModelForm):
        category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
        class Meta:
            model = inventoryItem
            fields = ['name','quantity', 'category']