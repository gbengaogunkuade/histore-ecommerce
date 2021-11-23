from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


# ADDED FIELDS
from django.core import validators
from PIL import Image
from django.utils import timezone
from django_countries.fields import CountryField            # for django countryfield
# from django_countries.widgets import CountrySelectWidget
# from datetime import datetime, date, time
from django.utils.text import slugify




# Create your models here.


today_date = timezone.now


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



# --------------------------------------------------------------------------------------
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200, default='Phones and Tablets')
    label = models.CharField(choices=LABEL_CHOICES, max_length=200, default='primary' )
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(default='default.jpg')
    added_date = models.DateTimeField(default=today_date)


    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Products"


    def __str__(self):
        return self.title



    # A "SAVE" FUNCTION TO OVERWRITE THE MODEL DEFAULT SAVE FUNCTION
    def save(self, *args, **kwargs):
        if self.discount:
            self.discount = self.discount
        else:
            self.discount = 0
        
        self.slug = slugify(self.title)             # SLUGIFY
        super().save(*args, **kwargs)


        
    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})

    def get_add_single_item_to_cart_url(self):
        return reverse('product:add_single_item_to_cart', kwargs={'slug': self.slug})

    def get_remove_single_item_from_cart_url(self):
        return reverse('product:remove_single_item_from_cart', kwargs={'slug': self.slug})

    def get_remove_items_from_cart_url(self):
        return reverse('product:remove_all_items_from_cart', kwargs={'slug': self.slug})





    def get_amount_saved(self):
        if self.discount:
            return self.price - self.discount
        else:
            pass
            

            


# --------------------------------------------------------------------------------------
class Menu(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_session_id = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=False, default=today_date)
    save_this_product = models.BooleanField(default=False)



    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Menu"
    

    def __str__(self):
        return f'{self.product.title} - {self.quantity}'



    def get_subtotal(self):
        price = self.product.price
        discount = self.product.discount
        quantity = self.quantity
        if discount:
            return discount * quantity
        else:
            return price * quantity


    def get_amount_saved(self):
        price = self.product.price
        discount = self.product.discount
        return price - discount







# --------------------------------------------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_session_id = models.TextField(null=True, blank=True)
    items = models.ManyToManyField(Menu)
    start_date = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(default=today_date)
    ordered = models.BooleanField(default=False)


    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Cart"
    


    def __str__(self):
        return "Cart"


    
    def get_total(self):
        total = 0
        for object in self.items.all():
            total = total + object.get_subtotal()
        return total


    def get_total_amount_saved(self):
        total_amount_saved = 0
        for menu_object in self.items.all():
            total_amount_saved = total_amount_saved + menu_object.get_amount_saved()
        return total_amount_saved







# ---------------------------------------------------------------------------------
# DELIVERY ADDRESS MODEL
# ---------------------------------------------------------------------------------

PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Cash', 'Cash')
)


COUNTRY_CHOICES = (
    ('Nigeria', 'Nigeria'),
    ('USA', 'USA'),
    ('Ghana', 'Ghana'),
)


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=400)
    zip = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200, default='')
    save_information = models.BooleanField(max_length=200, default=False)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=200)


    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name + ' ' + 'Delivery Address'
        name = name.title()
        return name


    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Delivery Address"








# ---------------------------------------------------------------------------------
# TEMPORARY ADDRESS MODEL
# ---------------------------------------------------------------------------------

PAYMENT_CHOICES = (
    ('Stripe', 'Stripe'),
    ('Cash', 'Cash')
)


COUNTRY_CHOICES = (
    ('Nigeria', 'Nigeria'),
    ('USA', 'USA'),
    ('Ghana', 'Ghana'),
)


class TemporaryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=200)
    zip = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200, default='')


    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name + ' ' + 'Temporary Address'
        name = name.title()
        return name


    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Temporary Address"











# ---------------------------------------------------------------------------------
# PURCHASED ITEM MODEL
# ---------------------------------------------------------------------------------

today_date = timezone.now


class Purchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(default=0, null=True, blank=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(default='default.jpg')
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=True)
    date_bought = models.DateTimeField(default=today_date)
    receiving_address = models.TextField(blank=True, null=True)
    delivered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.first_name + ' ' + 'Purchased'


    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Purchased"


    def get_purchased_subtotal(self):
        if self.discount:
            return self.discount * self.quantity
        else:
            return self.price * self.quantity








# ---------------------------------------------------------------------------------
# SAVED PRODUCT MODEL
# ---------------------------------------------------------------------------------

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



# --------------------------------------------------------------------------------------
class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200, default='Phones and Tablets')
    label = models.CharField(choices=LABEL_CHOICES, max_length=200, default='primary' )
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(default='default.jpg')
    added_date = models.DateTimeField(default=today_date)




    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "SavedProducts"


    def __str__(self):
        return self.title







# ---------------------------------------------------------------------------------
# VIEWED PRODUCT MODEL
# ---------------------------------------------------------------------------------
class ViewedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    user_session_id = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discount = models.IntegerField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=200, default='Phones and Tablets')
    label = models.CharField(choices=LABEL_CHOICES, max_length=200, default='primary' )
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    photo = models.URLField(default='default.jpg')
    added_date = models.DateTimeField(default=today_date)




    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "ViewedProducts"


    def __str__(self):
        return self.title






# ---------------------------------------------------------------------------------
# CONTACT MODEL
# ---------------------------------------------------------------------------------
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    address = models.CharField(max_length=200)
    message = models.TextField()




    # THE MODEL ADMIN "VERBOSE NAME PLURAL"
    class Meta:
        verbose_name_plural = "Contacts"


    def __str__(self):
        return self.first_name + ' ' + self.last_name
