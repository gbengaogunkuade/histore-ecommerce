from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError




































# # USER REGISTRATION FORM
# # - create a new form "FreeShopUserForm" from the
# # - builtin "UserCreationForm" of the builtin model "User"
# # - make sure to exclude the password1 and password2 fields from the form creation for security reasons
# class RegisterForm(forms.Form):
#     username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
#     first_name = forms.CharField(label='FirstName', widget=forms.TextInput(attrs={'placeholder':'FirstName', 'class':'form-control'}))
#     last_name = forms.CharField(label='LastName', widget=forms.TextInput(attrs={'placeholder':'LastName', 'class':'form-control'}))
#     email = forms.CharField(label='Email Address', widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'class':'form-control'}))
#     verify_email = forms.CharField(label='Verify Email Address', widget=forms.EmailInput(attrs={'placeholder':'Verify Email Address', 'class':'form-control'}))
#     password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))
#     verify_password = forms.CharField(label='Verify Password', widget=forms.PasswordInput(attrs={'placeholder':'Verify Password', 'class':'form-control'}))


#     # # VALIDATION CHECK OF MULTIPLE FIELDS AT ONCE
#     # # -----------------------------------------------------------------------------------
#     def clean(self):
#         cleaned_data = super().clean() 
#         return cleaned_data






# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
#     password1 = forms.CharField(label='Password1', widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'form-control'}))


#     # # VALIDATION CHECK OF MULTIPLE FIELDS AT ONCE
#     # # -----------------------------------------------------------------------------------
#     def clean(self):
#         cleaned_data = super().clean() 
#         return cleaned_data


