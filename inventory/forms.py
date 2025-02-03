from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import inventoryItem, Category,Department,Staff,IssueOut

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



class StaffForm(forms.ModelForm):
        department = forms.ModelChoiceField(queryset=Department.objects.all(), initial=0)
        class Meta:
            model = Staff
            fields = ['name','department',]




class IssueOutForm(forms.ModelForm):
     class Meta:
          model =IssueOut
          fields = ['inventoryItem', 'staff', 'quantity']
          
     def clean_quantity(self):                                                           #method for quantity validation    
        quantity = self.cleaned_data.get('quantity')                                     # it retrieves my inputted quanity
        inventory_item = self.cleaned_data.get('inventoryItem')                           #

        if inventory_item:
            available_quantity = inventory_item.quantity  # Fetch available stock
            if quantity > available_quantity:
                raise forms.ValidationError(f"Cannot issue more than {available_quantity} items.")
            if quantity <= 0:
                raise forms.ValidationError("Quantity must be greater than 0.")

        return quantity
     





class UploadForm(forms.Form):
     file = forms.FileField()