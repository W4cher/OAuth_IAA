# forms.py
from django import forms

class PasswordResetForm(forms.Form):
    token = forms.CharField(label='Token', max_length=100)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)