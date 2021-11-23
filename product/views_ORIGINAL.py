from django.shortcuts import render, redirect
from product.models import Product, Menu, Cart, PrivateBasket
from django.utils import timezone

# ADDED
import random
# from django.contrib.auth.models import User






# Create your views here.



# # ------------------------------------------------------------------------------------
# # HOME
# # ------------------------------------------------------------------------------------

# def homeview(request):

#     if request.user.is_authenticated:
#         baba = 'GOOD, YOU ARE LOGGED IN'
#     else:
#         baba = 'You are not logged in, please log in to enjoy a wonderful browsing experiene...'

#     objects = Product.objects.all()
#     context = {
#         'wording': 'THIS IS THE HOME PAGE',
#         'objects': objects,
#         'baba': baba
#     }
#     return render(request,'product/home.html', context)







# ------------------------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------------------------

def homeview(request):

    objects = Product.objects.all()

    context = {
        'wording': 'THIS IS THE HOME PAGE',
        'objects': objects,
    }  
    return render(request,'product/home.html', context)











# ------------------------------------------------------------------------------------
# CONTACT
# ------------------------------------------------------------------------------------

def contactview(request):

    context = {
        'wording': 'THIS IS THE CONTACT PAGE'
    }  
    return render(request,'product/contact.html', context)







# ------------------------------------------------------------------------------------
# DETAIL
# ------------------------------------------------------------------------------------

def detailview(request, slug):

    # CREATING SESSION ID FOR THE USER 
    # ---------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        user_session_id = random.randrange(0, 1000000)
        request.session['user_session_id'] = user_session_id
        print('NEW USER_SESSION_ID SET')
        print(request.session.get('user_session_id', None))
        
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    object, created = Product.objects.get_or_create(slug=slug)

    context = {
        'wording': 'THIS IS THE CONTACT PAGE',
        'object': object,
    }
    return render(request,'product/detail.html', context)







# ------------------------------------------------------------------------------------
# ADD SINGLE ITEM TO CART
# ------------------------------------------------------------------------------------

def add_single_item_to_cart(request, slug):
    
    # GET THE CURRENT_USER_SESSION_ID

    current_user_session_id = request.session.get('user_session_id', None)

    if current_user_session_id is None:
        print('USER DOES NOT HAVE SESSION_ID SET')
        return redirect('product:detail', slug=slug)   

    else:
        print('USER HAS A SESSION_ID')
        object, created = Product.objects.get_or_create(slug=slug)

        user_product, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
        
        cart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)
        
        if cart:

            current_cart = cart[0]

            if current_cart.items.all().filter(product__slug=object.slug):
                user_product.quantity += 1
                user_product.save()
                return redirect('product:detail', slug=slug)
            else:
                current_cart.items.add(user_product)    
                current_cart.save()
                return redirect('product:detail', slug=slug)
        else:
            today_date = timezone.now()
            new_cart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
            new_cart.items.add(user_product)   
            new_cart.save()
            return redirect('product:detail', slug=slug)








# ------------------------------------------------------------------------------------
# REMOVE SINGLE ITEM FROM CART
# ------------------------------------------------------------------------------------

def remove_single_item_from_cart(request, slug):
    
    # GET tTHE CURRENT_USER_SESSION_ID

    current_user_session_id = request.session.get('user_session_id', None)

    if current_user_session_id is None:
        print('USER DOES NOT HAVE SESSION_ID SET')
        return redirect('product:detail', slug=slug)   

    else:
        print('USER HAS A SESSION_ID')
        object, created = Product.objects.get_or_create(slug=slug)

        user_product, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
        
        cart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)
        
        if cart:

            current_cart = cart[0]

            if current_cart.items.all().filter(product__slug=object.slug):
                if user_product.quantity > 1:
                    user_product.quantity -= 1
                    user_product.save()
                    return redirect('product:detail', slug=slug)
                else:
                    current_cart.items.remove(user_product)
                    user_product.delete()

                    all_user_products = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                    if all_user_products:
                        # return to order_summary
                        return redirect('product:detail', slug=slug) 
                    else:
                        cart.delete()
                        return redirect('product:home')  
            else:
                return redirect('product:home')
        else:
            # delete user_product created when you run this view on an empty cart
            user_product.delete()       # to be removed...
            return redirect('product:home')





# ------------------------------------------------------------------------------------
# REMOVE ALL ITEMS FROM CART
# ------------------------------------------------------------------------------------

def remove_items_from_cart(request, slug):

    current_user_session_id = request.session.get('user_session_id', None)

    if current_user_session_id is None:
        print('USER DOES NOT HAVE SESSION_ID SET')
        return redirect('product:detail', slug=slug)

    else:
        print('USER HAS A SESSION ID')
        object, created = Product.objects.get_or_create(slug=slug)

        user_product, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

        cart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

        if cart:
            current_cart = cart[0]

            if current_cart.items.all().filter(product__slug=object.slug):
                current_cart.items.remove(user_product)
                user_product.delete()

                all_user_products = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                if all_user_products:
                    # return to order_summary
                    return redirect('product:detail', slug=slug) 
                else:
                    cart.delete()
                    return redirect('product:home') 
                        
            else:
                return redirect('product:detail', slug=slug)

        else:
            # delete user_product created when you run this view on an empty cart
            user_product.delete()       # to be removed...
            return redirect('product:home')
            






# ------------------------------------------------------------------------------------
# ORDER_SUMMARY
# ------------------------------------------------------------------------------------

def order_summary(request):

    current_user_session_id = request.session.get('user_session_id', None)

    if current_user_session_id is None:
        print('NO USER SESSION FOUND')
        return redirect('product:home')
    else:
        cart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

        if cart:
            current_cart = cart[0]
            objects = current_cart.items.all()
            objects = objects.order_by('-added_date')

        else:           
            print('NO ITEM IN THE CART YET')
            return redirect('product:home')

    context = {
        'objects': objects
        }

    return render(request, 'product/order_summary.html', context)









