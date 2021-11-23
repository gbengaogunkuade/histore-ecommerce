from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from product.models import Product, DeliveryAddress, Contact
from django_countries.fields import CountryField
from django.contrib.auth.models import User






CATEGORY_CHOICES = (
    ('Computer and Electronics', 'Computer and Electronics'),
    ('Phones and Tablets', 'Phones and Tablets'),
    ('Fashions and Styles', 'Fashions and Styles'),
    ('Home and Kitchen', 'Home and Kitchen'),
    ('Drinks and Wine', 'Drinks and Wine'),
    ('Kids and Toys', 'Kids and Toys'),
    ('Others', 'Others')
)


LABEL_CHOICES = (
    ('primary', 'PRIMARY'),
    ('secondary', 'SECONDARY'),
    ('danger', 'DANGER')
)



# -----------------------------------------------------------------------------------
# PRODUCT FORM
# -----------------------------------------------------------------------------------

class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'W34 Bluetooth Call Smart Watch ECG Heart Rate', 'class':'form-control'}), required=True)
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'1000', 'class':'form-control'}), required=True)
    discount = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'0', 'class':'form-control'}), required=False)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=True, initial='hot sales')
    label = forms.ChoiceField(choices=LABEL_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=True, initial='primary')
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description...', 'class':'form-control'}), required=False)
    photo = forms.CharField(widget=forms.URLInput(attrs={'placeholder':'https://product/57857354.jpg', 'class':'form-control'}), required=True)


    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        model = Product
        # fields = '__all__'

        fields = [
            'title',
            'price',
            'discount',
            'category',
            'label',
            'description',
            'photo',
        ]
        







# -----------------------------------------------------------------------------------
# DELIVERY ADDRESS FORM
# -----------------------------------------------------------------------------------

PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Cash', 'Cash')
)


COUNTRY_CHOICES = (
    ('Nigeria', 'Nigeria'),
    ('USA', 'USA'),
    ('Ghana', 'Ghana'),
)



class DeliveryAddressForm(forms.ModelForm):
    address1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'20 Johnson Street', 'class':'form-control'}))
    address2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Ojodu Berger, Lagos', 'class':'form-control'}), required=False)
    # country = CountryField(blank_label='(select country)').formfield()
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=True, initial='Nigeria')
    zip = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'111001', 'class':'form-control'}))
    telephone = forms.CharField(widget=forms.NumberInput(attrs={'placeholder':'08042241125', 'class':'form-control'}))
    save_information = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked'}), required=False)
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())



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
            'telephone',
            'save_information',
            'payment_option',
        ]




class ContactForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username', 'class':'form-control'}), required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'FirstName', 'class':'form-control'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'LastName', 'class':'form-control'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Block 154 Johnson Street, Ikeja Lagos, Nigeria', 'class':'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Description...', 'class':'form-control'}), required=False)




    # validation check of multiple fields at once
    # -----------------------------------------------------------------------------------
    def clean(self):
        cleaned_data = super().clean() 
        return cleaned_data


    class Meta:
        model = Contact
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'address',
            'message',
        ]
