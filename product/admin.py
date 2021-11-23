from django.contrib import admin
from product.models import Product, Menu, Cart, DeliveryAddress, TemporaryAddress, Purchased, SavedProduct, ViewedProduct, Contact


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['user', 'title', 'price', 'discount', 'added_date', 'quantity']
    list_display_links = ['title']



class MenuAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_session_id', 'product', 'quantity', 'ordered', 'save_this_product']
    list_display_links = ['product']



class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_session_id', 'created_date', 'ordered']
    list_display_links = ['user', 'user_session_id']



class PurchasedAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'quantity', 'ordered', 'date_bought', 'delivered']
    list_display_links = ['user', 'title']


class ViewedProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_session_id', 'title', 'quantity', 'added_date']
    list_display_links = ['title']



class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'address']
    list_display_links = ['last_name']







admin.site.register(Product, ProductAdmin)

admin.site.register(Menu, MenuAdmin)

admin.site.register(Cart, CartAdmin)

admin.site.register(DeliveryAddress)

admin.site.register(TemporaryAddress)

admin.site.register(Purchased, PurchasedAdmin)

admin.site.register(SavedProduct)

admin.site.register(ViewedProduct, ViewedProductAdmin)

admin.site.register(Contact, ContactAdmin)








