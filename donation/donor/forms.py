from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField()
    phone_number = forms.CharField(max_length=20)
    blood_type = forms.CharField(max_length=10)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'age', 'phone_number', 'blood_type', 'username', 'password1', 'password2']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['phone', 'sex', 'age', 'blood', 'pint', 'reason']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['phone', 'blood', 'pint']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'sex', 'age', 'image']
