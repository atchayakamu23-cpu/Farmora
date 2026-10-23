from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))
    phone = forms.CharField(max_length=15)
