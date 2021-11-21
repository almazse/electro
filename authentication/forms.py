from django import forms
from shop.models import Product
from cart.models import Order


class UserLoginForm(forms.Form):
    login = forms.CharField(required=False)
    password = forms.CharField(required=False, initial=False, widget=forms.PasswordInput)


class AdminAddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ("category", "brand", "name", "slug", "main_photo", "photo_1", "photo_2", "photo_3", "description",
                  "details", "price", "old_price", "stock", "available", "rait")


class AdminPaidStatusForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ("paid", )
