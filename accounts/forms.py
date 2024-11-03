from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'first_name','last_name', 'phone_number','password1','password2')

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('passwords must match!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='you can change your password in '
                                                   '<a href="../password">this link </a>')

    class Meta:
        model = User
        fields = ('phone_number', 'password','first_name','last_name','email','address','last_login',
                  'is_active','is_admin')


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}),required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=True)

    def clean_email(self):
        user_email = self.cleaned_data.get('email')
        if User.objects.filter(email=user_email).exists():
            raise ValidationError('email must be unique')
        return user_email

    def clean_phone_number(self):
        user_phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=user_phone_number).exists():
            raise ValidationError('Phone number must be unique')
        return user_phone_number

    def clean(self):
        cd = super().clean()
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('passwords must match!')


class OtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),required=True)


class UserUpdateForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('first_name','last_name','email','address')