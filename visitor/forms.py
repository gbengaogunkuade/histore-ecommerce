from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from product.models import DeliveryAddress


from django.core.exceptions import ValidationError



# -----------------------------------------------------------------------------------
# REGISTER FORM
# -----------------------------------------------------------------------------------

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'FirstName', 'class':'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'LastName', 'class':'form-control'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control'}), required=True)
    verify_email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Verify Email', 'class':'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'', 'class':'form-control'}), required=True)
    verify_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'', 'class':'form-control'}), required=True)


    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        model = User
        fields = '__all__'
        # fields = [
        #     'username',
        #     'first_name',
        #     'last_name',
        #     'email',
        #     'verify_email',
        #     'password',
        #     'verify_password',
        # ]





# -----------------------------------------------------------------------------------
# Login Form
# -----------------------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'', 'class':'form-control'}), required=True)



    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        fields = '__all__'







# -----------------------------------------------------------------------------------
# UserProfileForm
# -----------------------------------------------------------------------------------

class UserProfileForm(forms.ModelForm):
    new_username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Leave blank if you don\'t want to change your username', 'class':'form-control'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'FirstName', 'class':'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'LastName', 'class':'form-control'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control'}), required=True)
    

    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        model = User
        fields = [
            'new_username', 
            'first_name', 
            'last_name', 
            'email'
            ]




# -----------------------------------------------------------------------------------
# UserAddressForm
# -----------------------------------------------------------------------------------

COUNTRY_CHOICES = (
    ('Nigeria', 'Nigeria'),
    ('USA', 'USA'),
    ('Ghana', 'Ghana'),
)


class UserAddressForm(forms.ModelForm):
    address1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'20 Johnson Street', 'class':'form-control'}), required=True)
    address2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Ojodu Berger, Lagos', 'class':'form-control'}), required=False)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=True, initial='Nigeria')
    zip = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'111001', 'class':'form-control'}), required=True)
    telephone = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'08042241125', 'class':'form-control'}), required=True)
    

    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        model = DeliveryAddress
        fields = [
            'address1',
            'address2',
            'country',
            'zip',
            'telephone'
        ]








# # -----------------------------------------------------------------------------------
# # Logic Answer Form
# # -----------------------------------------------------------------------------------

# class LogicAnswerForm(forms.Form):
#     first_number = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'result', 'class':'form-control'}), required=True)

    
    












