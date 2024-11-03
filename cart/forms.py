from django import forms

from accounts.models import User


class CartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number','first_name', 'last_name','address')

    def validate_unique(self):
        pass


class CouponForm(forms.Form):
    code = forms.CharField()