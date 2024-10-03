
from django import forms
from .models import Store
from .models import Items
class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'location', 'status', 'image','is_hidden']  # Include all the fields you want to edit
        widgets = {
            'status': forms.Select(choices=[('Active', 'Active'), ('Inactive', 'Inactive')]),
        }



class ItemForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['name', 'image', 'uploaded_by', 'discount']  # Add fields as necessary
