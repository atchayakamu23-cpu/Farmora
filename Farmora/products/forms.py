from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "quantity",
            "unit",
            "image",
            "available",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
