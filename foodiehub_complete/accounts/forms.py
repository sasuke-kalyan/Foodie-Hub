from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, DeliveryAddress


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=[('customer', 'Customer'), ('owner', 'Restaurant Owner')])

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['role'].widget.attrs['class'] = 'form-select'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['label', 'address_line', 'city', 'state', 'pincode', 'latitude', 'longitude', 'is_default']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['is_default'].widget.attrs['class'] = 'form-check-input'
