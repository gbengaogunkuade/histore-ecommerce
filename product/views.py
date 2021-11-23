from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Menu, Cart, DeliveryAddress, TemporaryAddress, Purchased, SavedProduct, ViewedProduct, Contact
from product.forms import ProductForm, DeliveryAddressForm, ContactForm
from django.utils import timezone

# ADDED
import random
# from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib import messages             # messages alert

import os # NEW
import stripe   # import stripe
from django.conf import settings     # import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger        # PAGINATOR



# Create your views here.



# assign the imported stripe_Secret_key to a variable
stripe.api_key = settings.STRIPE_SECRET_KEY







# ------------------------------------------------------------------------------------
# HOME
# ------------------------------------------------------------------------------------

def home(request):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------

    # POST method
    if request.method == 'POST':
        lookup_word = request.POST['lookup_word']

        if lookup_word:

            if len(lookup_word) >= 3:

                objects = Product.objects.filter(title__icontains=lookup_word) | Product.objects.filter(description__icontains=lookup_word)

                num_of_objects = objects.count()

                
                if objects:

                    context = {
                    'lookup_word': lookup_word,
                    'objects': objects,
                    'num_of_objects': num_of_objects
                    }

                    messages.success(request, f'Congrats, we found "{num_of_objects}" products with keyword "{lookup_word}"')
                    return render(request, 'product/search.html', context)

                else:
                    messages.error(request, f'Sorry, we presently do not have what you are looking for with "{lookup_word}"')
                    return redirect('product:search')

            else:
                messages.info(request, f'There is no result for "{lookup_word}", search keyword must be atleast 3 characters long')
                return redirect('product:search')

        else:
            messages.info(request, f'You did not type any search keyword, search keyword must be atleast 3 characters long')
            return redirect('product:search')


    # GET method
    else:
        
        objects = Product.objects.all()
        objects = objects.order_by('-added_date')

        context = {
            'objects': objects
        }  
        return render(request,'product/home.html', context)






# ------------------------------------------------------------------------------------
# CONTACT
# ------------------------------------------------------------------------------------
def contact(request):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------

    # POST method
    if request.method == 'POST':
        logic_answer = request.POST['logic_answer']
        logic_answer = int(logic_answer)

        user_answer = request.POST['user_answer']
        user_answer = int(user_answer)

        form = ContactForm(request.POST)

        if logic_answer == user_answer:
        
            if form.is_valid():
                if request.user.is_authenticated:
                    first_name = form.cleaned_data['first_name']
                    newform = form.save(commit=False)
                    newform.user = request.user
                    newform.save()
                    messages.success(request, f'Dear {first_name}, your message has been submitted!')
                    return redirect('product:home')
                else:
                    first_name = form.cleaned_data['first_name']
                    form.save()
                    messages.success(request, f'Dear {first_name}, your message has been submitted!')
                    return redirect('product:home')

            else:
                messages.error(request, 'Invalid Data Submitted!')
                return redirect('product:contact')

        else:
            messages.error(request, 'Wrong Answer Submitted!')
            return redirect('product:contact')

    # GET method
    else:
        first_Number = random.randrange(4, 35)
        second_Number = random.randrange(11, 72)
        logic_answer = first_Number + second_Number

        form = ContactForm()
        context = {
            'form': form,
            'first_Number': first_Number,
            'second_Number': second_Number,
            'logic_answer': logic_answer,
            }
        return render(request,'product/contact.html', context)



    







# ------------------------------------------------------------------------------------
# DETAIL
# ------------------------------------------------------------------------------------

# def detail(request, slug):

#     # CREATE/GET USER_SESSION_ID
#     # ----------------------------------------------------------------------
#     # get the user_session_id
#     user_session_id = request.session.get('user_session_id', None)

#     if user_session_id is None:
#         # create a new user_session_id
#         generated_Number = random.randrange(0, 1000000)
#         request.session['user_session_id'] = generated_Number
#     else:
#         # print the user_session_id
#         print(request.session.get('user_session_id', None))
#     # ----------------------------------------------------------------------


#     # POST STATEMENT .......................................
#     if request.method == 'POST':

#         # IF USER IS AUTHENTICATED.................................
#         if request.user.is_authenticated:

#             current_user_session_id = request.session.get('user_session_id', None)

#             object, created = Product.objects.get_or_create(slug=slug)

#             user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)

#             quantity = request.POST['form_quantity']
#             quantity = int(quantity)

#             if quantity >= 1:

#                 cart = Cart.objects.filter(user=request.user, ordered=False)

#                 if cart:
#                     current_cart = cart[0]

#                     if current_cart.items.all().filter(product__slug=object.slug):
#                         user_object.quantity += quantity
#                         user_object.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)
#                     else:
#                         user_object.quantity = quantity
#                         user_object.save()
#                         current_cart.items.add(user_object)
#                         current_cart.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)

#                 else:
#                     today_date = timezone.now()
#                     user_object.quantity = quantity
#                     user_object.save()
#                     newcart = Cart.objects.create(user=request.user, created_date=today_date)
#                     newcart.items.add(user_object)
                    
#                     tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                     if tempMenu:
#                         for police in tempMenu:
#                             newcart.items.add(police)
#                     newcart.save()
#                     messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)

#             else:
#                 print('INVALID QUANTITY')
#                 return redirect('product:detail', slug=slug)


#         # IF USER IS NOT AUTHENTICATED.......................
#         else:

#             current_user_session_id = request.session.get('user_session_id', None)

#             object, created = Product.objects.get_or_create(slug=slug)

#             session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

#             quantity = request.POST['form_quantity']
#             quantity = int(quantity)

#             if quantity >= 1:

#                 tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                 if tempcart:
#                     current_tempcart = tempcart[0]

#                     if current_tempcart.items.all().filter(product__slug=object.slug):
#                         session_object.quantity += quantity
#                         session_object.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)
#                     else:
#                         session_object.quantity = quantity
#                         session_object.save()
#                         current_tempcart.items.add(session_object)
#                         current_tempcart.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)

#                 else:
#                     today_date = timezone.now()
#                     session_object.quantity = quantity
#                     session_object.save()
#                     newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
#                     newtempcart.items.add(session_object)
#                     newtempcart.save()
#                     messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)
#             else:
#                 print('INVALID QUANTITY')
#                 return redirect('product:detail', slug=slug)



#     # GET STATEMENT.......................
#     else:
#         if request.user.is_authenticated:

#             object, created = Product.objects.get_or_create(slug=slug)

#             object_category = object.category

#             # the saved object
#             saved_object = SavedProduct.objects.filter(user=request.user, slug=object.slug)

#             # the object owner i.e. the person who posted the product
#             object_owner = object.user

#             # related objects
#             related_objects = Product.objects.filter(category=object_category)

#             context = {
#                 'object': object,
#                 'object_owner': object_owner,
#                 'visitor': request.user,
#                 'saved_object': saved_object,
#                 'related_objects': related_objects,
#             }
#             return render(request,'product/detail.html', context)
        

#         else:
#             object, created = Product.objects.get_or_create(slug=slug)

#             object_category = object.category

#             # related objects
#             related_objects = Product.objects.filter(category=object_category)

#             context = {
#                 'object': object,
#                 'visitor': request.user,
#                 'related_objects': related_objects
#             }
#             return render(request,'product/detail.html', context)





# def detail(request, slug):

#     # CREATE/GET USER_SESSION_ID
#     # ----------------------------------------------------------------------
#     # get the user_session_id
#     user_session_id = request.session.get('user_session_id', None)

#     if user_session_id is None:
#         # create a new user_session_id
#         generated_Number = random.randrange(0, 1000000)
#         request.session['user_session_id'] = generated_Number
#     else:
#         # print the user_session_id
#         print(request.session.get('user_session_id', None))
#     # ----------------------------------------------------------------------


#     # POST STATEMENT .......................................
#     if request.method == 'POST':

#         # IF USER IS AUTHENTICATED.................................
#         if request.user.is_authenticated:

#             current_user_session_id = request.session.get('user_session_id', None)

#             object, created = Product.objects.get_or_create(slug=slug)

#             user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)

#             quantity = request.POST['form_quantity']
#             quantity = int(quantity)

#             if quantity >= 1:

#                 cart = Cart.objects.filter(user=request.user, ordered=False)

#                 if cart:
#                     current_cart = cart[0]

#                     if current_cart.items.all().filter(product__slug=object.slug):
#                         user_object.quantity += quantity
#                         user_object.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)
#                     else:
#                         user_object.quantity = quantity
#                         user_object.save()
#                         current_cart.items.add(user_object)
#                         current_cart.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)

#                 else:
#                     today_date = timezone.now()
#                     user_object.quantity = quantity
#                     user_object.save()
#                     newcart = Cart.objects.create(user=request.user, created_date=today_date)
#                     newcart.items.add(user_object)
                    
#                     tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                     if tempMenu:
#                         for police in tempMenu:
#                             newcart.items.add(police)
#                     newcart.save()
#                     messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)

#             else:
#                 print('INVALID QUANTITY')
#                 return redirect('product:detail', slug=slug)


#         # IF USER IS NOT AUTHENTICATED.......................
#         else:

#             current_user_session_id = request.session.get('user_session_id', None)

#             object, created = Product.objects.get_or_create(slug=slug)

#             session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

#             quantity = request.POST['form_quantity']
#             quantity = int(quantity)

#             if quantity >= 1:

#                 tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                 if tempcart:
#                     current_tempcart = tempcart[0]

#                     if current_tempcart.items.all().filter(product__slug=object.slug):
#                         session_object.quantity += quantity
#                         session_object.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                         return redirect('product:detail', slug=slug)
#                     else:
#                         session_object.quantity = quantity
#                         session_object.save()
#                         current_tempcart.items.add(session_object)
#                         current_tempcart.save()
#                         messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)

#                 else:
#                     today_date = timezone.now()
#                     session_object.quantity = quantity
#                     session_object.save()
#                     newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
#                     newtempcart.items.add(session_object)
#                     newtempcart.save()
#                     messages.success(request, f'{quantity} - {object.title} added to cart')
#                     return redirect('product:detail', slug=slug)
#             else:
#                 print('INVALID QUANTITY')
#                 return redirect('product:detail', slug=slug)



#     # GET STATEMENT.......................
#     else:
#         if request.user.is_authenticated:

#             object, created = Product.objects.get_or_create(slug=slug)

#             object_category = object.category

#             # the saved object
#             saved_object = SavedProduct.objects.filter(user=request.user, slug=object.slug)


#             # -------------------------------------------------------------------------
#             # the current_view_object

#             current_viewed_object = ViewedProduct.objects.filter(user=request.user, user_session_id=user_session_id, slug=object.slug)

#             # current_viewed_object = ViewedProduct.objects.filter(user=request.user, slug=object.slug) or ViewedProduct.objects.filter(user_session_id=user_session_id, slug=object.slug)

#             if current_viewed_object:
#                 pass

#             else:
#                 current_viewed_object = ViewedProduct.objects.create(
#                     user = request.user,
#                     user_session_id=user_session_id,
#                     title = object.title,
#                     price = object.price,
#                     discount = object.discount,
#                     quantity = object.quantity,
#                     category = object.category,
#                     label = object.label,
#                     slug = object.slug,
#                     description = object.description,
#                     photo = object.photo
#                     )

#                 current_viewed_object.save()

#             # all_viewed_objects = ViewedProduct.objects.filter(user_session_id=user_session_id)
#             all_viewed_objects = ViewedProduct.objects.filter(user=request.user) | ViewedProduct.objects.filter(user_session_id=user_session_id)

#             all_viewed_objects = all_viewed_objects.order_by('-added_date')

#             # six recently viewed products
#             all_viewed_objects = all_viewed_objects[0:6]
            
#             # the object owner i.e. the person who posted the product
#             object_owner = object.user

#             current_object_slug = object.slug
   
#             # related objects
#             related_objects = Product.objects.filter(category=object_category).exclude(slug=current_object_slug)


#             context = {
#                 'object': object,
#                 'object_owner': object_owner,
#                 'visitor': request.user,
#                 'saved_object': saved_object,
#                 'related_objects': related_objects,
#                 'all_viewed_objects': all_viewed_objects
#             }
#             return render(request,'product/detail.html', context)
        

#         else:
#             object, created = Product.objects.get_or_create(slug=slug)

#             object_category = object.category


#             # -------------------------------------------------------------------------
#             # the current_view_object
            
#             current_viewed_object = ViewedProduct.objects.filter(user_session_id=user_session_id, slug=object.slug)

#             if current_viewed_object:
#                 pass

#             else:
#                 current_viewed_object = ViewedProduct.objects.create(
#                     user_session_id=user_session_id,
#                     title = object.title,
#                     price = object.price,
#                     discount = object.discount,
#                     quantity = object.quantity,
#                     category = object.category,
#                     label = object.label,
#                     slug = object.slug,
#                     description = object.description,
#                     photo = object.photo
#                     )

#                 current_viewed_object.save()

#             # the viewed products
#             all_viewed_objects = ViewedProduct.objects.filter(user_session_id=user_session_id)

#             all_viewed_objects = all_viewed_objects.order_by('-added_date')

#             # six recently viewed products
#             all_viewed_objects = all_viewed_objects[0:6]
            

#             current_object_slug = object.slug
   
#             # related objects
#             related_objects = Product.objects.filter(category=object_category).exclude(slug=current_object_slug)

#             context = {
#                 'object': object,
#                 'visitor': request.user,
#                 'related_objects': related_objects,
#                 'all_viewed_objects': all_viewed_objects
#             }
#             return render(request,'product/detail.html', context)









def detail(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------


    # POST STATEMENT .......................................
    if request.method == 'POST':

        # IF USER IS AUTHENTICATED.................................
        if request.user.is_authenticated:

            current_user_session_id = request.session.get('user_session_id', None)

            object, created = Product.objects.get_or_create(slug=slug)

            user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)

            quantity = request.POST['form_quantity']
            quantity = int(quantity)

            if quantity >= 1:

                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    current_cart = cart[0]

                    if current_cart.items.all().filter(product__slug=object.slug):
                        user_object.quantity += quantity
                        user_object.save()
                        messages.success(request, f'{quantity} - {object.title} added to cart')
                        return redirect('product:detail', slug=slug)
                    else:
                        user_object.quantity = quantity
                        user_object.save()
                        current_cart.items.add(user_object)
                        current_cart.save()
                        messages.success(request, f'{quantity} - {object.title} added to cart')
                        return redirect('product:detail', slug=slug)

                else:
                    today_date = timezone.now()
                    user_object.quantity = quantity
                    user_object.save()
                    newcart = Cart.objects.create(user=request.user, created_date=today_date)
                    newcart.items.add(user_object)
                    
                    tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                    if tempMenu:
                        for police in tempMenu:
                            newcart.items.add(police)
                    newcart.save()
                    messages.success(request, f'{quantity} - {object.title} added to cart')
                    return redirect('product:detail', slug=slug)

            else:
                print('INVALID QUANTITY')
                return redirect('product:detail', slug=slug)


        # IF USER IS NOT AUTHENTICATED.......................
        else:

            current_user_session_id = request.session.get('user_session_id', None)

            object, created = Product.objects.get_or_create(slug=slug)

            session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

            quantity = request.POST['form_quantity']
            quantity = int(quantity)

            if quantity >= 1:

                tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

                if tempcart:
                    current_tempcart = tempcart[0]

                    if current_tempcart.items.all().filter(product__slug=object.slug):
                        session_object.quantity += quantity
                        session_object.save()
                        messages.success(request, f'{quantity} - {object.title} added to cart')
                        return redirect('product:detail', slug=slug)
                    else:
                        session_object.quantity = quantity
                        session_object.save()
                        current_tempcart.items.add(session_object)
                        current_tempcart.save()
                        messages.success(request, f'{quantity} - {object.title} added to cart')
                    return redirect('product:detail', slug=slug)

                else:
                    today_date = timezone.now()
                    session_object.quantity = quantity
                    session_object.save()
                    newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
                    newtempcart.items.add(session_object)
                    newtempcart.save()
                    messages.success(request, f'{quantity} - {object.title} added to cart')
                    return redirect('product:detail', slug=slug)
            else:
                print('INVALID QUANTITY')
                return redirect('product:detail', slug=slug)



    # GET STATEMENT.......................
    else:
        if request.user.is_authenticated:

            object, created = Product.objects.get_or_create(slug=slug)

            object_category = object.category

            # the saved object
            saved_object = SavedProduct.objects.filter(user=request.user, slug=object.slug)


            # -------------------------------------------------------------------------
            # the viewed object logic
            temp_viewed_objects = ViewedProduct.objects.filter(user_session_id=user_session_id)

            # get the viewed session objects and create it for the user 
            if temp_viewed_objects:
                for temp_object in temp_viewed_objects:
                    current_temp_viewed_object = ViewedProduct.objects.create(
                        user = request.user,
                        user_session_id=user_session_id,
                        title = temp_object.title,
                        price = temp_object.price,
                        discount = temp_object.discount,
                        quantity = temp_object.quantity,
                        category = temp_object.category,
                        label = temp_object.label,
                        slug = temp_object.slug,
                        description = temp_object.description,
                        photo = temp_object.photo
                        )

                    current_temp_viewed_object.save()
                    temp_object.delete() # delete the session object
            else:
                pass

            # get the current user viewd object
            current_viewed_object = ViewedProduct.objects.filter(user=request.user, slug=object.slug)

            if current_viewed_object:
                pass

            else:
                current_viewed_object = ViewedProduct.objects.create(
                    user = request.user,
                    user_session_id=user_session_id,
                    title = object.title,
                    price = object.price,
                    discount = object.discount,
                    quantity = object.quantity,
                    category = object.category,
                    label = object.label,
                    slug = object.slug,
                    description = object.description,
                    photo = object.photo
                    )

                current_viewed_object.save()

            # all viewed products
            all_viewed_objects = ViewedProduct.objects.filter(user=request.user)

            all_viewed_objects = all_viewed_objects.order_by('-added_date')

            # eight recently viewed products
            all_viewed_objects = all_viewed_objects[0:4]
            
            # the object owner i.e. the person who posted the product
            object_owner = object.user

            current_object_slug = object.slug
   
            # related objects
            related_objects = Product.objects.filter(category=object_category).exclude(slug=current_object_slug)

            # eight related products
            related_objects = related_objects[0:4]


            context = {
                'object': object,
                'object_owner': object_owner,
                'visitor': request.user,
                'saved_object': saved_object,
                'related_objects': related_objects,
                'all_viewed_objects': all_viewed_objects
            }
            return render(request,'product/detail.html', context)
        


        else:
            object, created = Product.objects.get_or_create(slug=slug)

            object_category = object.category


            # -------------------------------------------------------------------------
            # the viewed object logic
            
            current_viewed_object = ViewedProduct.objects.filter(user_session_id=user_session_id, slug=object.slug)

            if current_viewed_object:
                pass

            else:
                current_viewed_object = ViewedProduct.objects.create(
                    user_session_id=user_session_id,
                    title = object.title,
                    price = object.price,
                    discount = object.discount,
                    quantity = object.quantity,
                    category = object.category,
                    label = object.label,
                    slug = object.slug,
                    description = object.description,
                    photo = object.photo
                    )

                current_viewed_object.save()

            # all viewed products
            all_viewed_objects = ViewedProduct.objects.filter(user_session_id=user_session_id)

            all_viewed_objects = all_viewed_objects.order_by('-added_date')

            # eight recently viewed products
            all_viewed_objects = all_viewed_objects[0:4]
            

            current_object_slug = object.slug
   
            # related objects
            related_objects = Product.objects.filter(category=object_category).exclude(slug=current_object_slug)

            # eight related products
            related_objects = related_objects[0:4]

            context = {
                'object': object,
                'visitor': request.user,
                'related_objects': related_objects,
                'all_viewed_objects': all_viewed_objects
            }
            return render(request,'product/detail.html', context)















# ------------------------------------------------------------------------------------
# ADD SINGLE ITEM TO CART
# ------------------------------------------------------------------------------------

def add_single_item_to_cart(request, slug):

    # IF USER IS AUTHENTICATED................................
    if request.user.is_authenticated:
        
            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            if current_user_session_id is None:
                print('USER DOES NOT HAVE SESSION_ID SET')
                return redirect('product:detail', slug=slug)   
            else:
                print('USER HAS A SESSION_ID')

                object, created = Product.objects.get_or_create(slug=slug)

                user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
                
                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    current_cart = cart[0]

                    if current_cart.items.all().filter(product__slug=object.slug):                   
                        user_object.quantity += 1
                        user_object.save()
                        messages.success(request, 'Item Quantity Increased')
                        return redirect('product:order_summary') 

                    else:
                        current_cart.items.add(user_object)
                        current_cart.save()
                        return redirect('product:order_summary')

                else:
                    today_date = timezone.now()
                    newcart = Cart.objects.create(user=request.user, created_date=today_date)
                    newcart.items.add(user_object)
                    newcart.save()
                    return redirect('product:order_summary')


    # IF USER IS NOT AUTHENTICATED................................
    else:

        # GET THE CURRENT_USER_SESSION_ID
        current_user_session_id = request.session.get('user_session_id', None)

        if current_user_session_id is None:
            print('USER DOES NOT HAVE SESSION_ID SET')
            return redirect('product:detail', slug=slug)   

        else:
            print('USER HAS A SESSION_ID')

            object, created = Product.objects.get_or_create(slug=slug)

            session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)


            # ATTENDING TO TEMPCART
            if tempcart:
                current_tempcart = tempcart[0]

                if current_tempcart.items.all().filter(product__slug=object.slug):
                    session_object.quantity += 1		
                    session_object.save()
                    messages.success(request, 'Item Quantity Increased')
                    return redirect('product:order_summary')
                else:
                    current_tempcart.items.add(session_object)
                    current_tempcart.save()
                    return redirect('product:order_summary')

            else:
                today_date = timezone.now()
                newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
                newtempcart.items.add(session_object)
                newtempcart.save()
                return redirect('product:order_summary')









# ------------------------------------------------------------------------------------
# REMOVE SINGLE ITEM FROM CART
# ------------------------------------------------------------------------------------

def remove_single_item_from_cart(request, slug):
    
    # IF USER IS AUTHENTICATED................................
    if request.user.is_authenticated:
        
            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            if current_user_session_id is None:
                print('USER DOES NOT HAVE SESSION_ID')
                return redirect('product:detail', slug=slug)   
            else:
                print('USER HAS A SESSION_ID')

                object, created = Product.objects.get_or_create(slug=slug)

                user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
                
                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    current_cart = cart[0]

                    if current_cart.items.all().filter(product__slug=object.slug):
                        if user_object.quantity > 1:                  
                            user_object.quantity -= 1
                            user_object.save()
                            messages.error(request, 'Item Quantity Decreased')
                            return redirect('product:order_summary') 
                        else:
                            current_cart.items.remove(user_object)
                            user_object.delete()
                            messages.error(request, 'Item Deleted')

                            all_user_objects = Menu.objects.filter(user=request.user, ordered=False)

                            if all_user_objects:
                                return redirect('product:order_summary')  
                            else:
                                # current_cart.delete()      # DISABLE THIS LINE SO {% empty %} can work inside the Template
                                # cart.delete()             # DISABLE THIS LINE SO {% empty %} can work inside the Template
                                return redirect('product:order_summary')  
                    else:
                        return redirect('product:order_summary') 

                else:
                    # delete user_object created when you run this view on an empty cart
                    user_object.delete()       # to be removed...
                    return redirect('product:order_summary')


    # IF USER IS NOT AUTHENTICATED................................
    else:

        # GET THE CURRENT_USER_SESSION_ID
        current_user_session_id = request.session.get('user_session_id', None)

        if current_user_session_id is None:
            print('USER DOES NOT HAVE SESSION_ID SET')
            return redirect('product:detail', slug=slug)   
        else:
            print('USER HAS A SESSION_ID')

            object, created = Product.objects.get_or_create(slug=slug)

            session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
            
            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

            if tempcart:
                current_tempcart = tempcart[0]

                if current_tempcart.items.all().filter(product__slug=object.slug):
                    if session_object.quantity > 1:                  
                        session_object.quantity -= 1
                        session_object.save()
                        messages.error(request, 'Item Quantity Decreased')
                        return redirect('product:order_summary') 
                    else:
                        current_tempcart.items.remove(session_object)
                        session_object.delete()
                        messages.error(request, 'Item Deleted')

                        all_session_objects = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                        if all_session_objects:
                            return redirect('product:order_summary')  
                        else:
                            current_tempcart.delete()
                            tempcart.delete()
                            return redirect('product:order_summary')  
                else:
                    return redirect('product:order_summary') 

            else:
                # delete user_object created when you run this view on an empty cart
                session_object.delete()       # to be removed...
                return redirect('product:order_summary')







# ------------------------------------------------------------------------------------
# REMOVE ALL ITEMS FROM CART
# ------------------------------------------------------------------------------------

def remove_items_from_cart(request, slug):

# IF USER IS AUTHENTICATED................................
    if request.user.is_authenticated:
        
            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            if current_user_session_id is None:
                print('USER DOES NOT HAVE SESSION_ID')
                return redirect('product:detail', slug=slug)   
            else:
                print('USER HAS A SESSION_ID')

                object, created = Product.objects.get_or_create(slug=slug)

                user_object, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
                
                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    current_cart = cart[0]

                    if current_cart.items.all().filter(product__slug=object.slug):
                        current_cart.items.remove(user_object)
                        user_object.delete()
                        messages.error(request, 'Item Deleted')

                        all_session_objects = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                        if all_session_objects:
                            return redirect('product:order_summary')  
                        else:
                            # current_cart.delete()      # DISABLE THIS LINE SO {% empty %} can work inside the Template
                            # cart.delete()             # DISABLE THIS LINE SO {% empty %} can work inside the Template
                            return redirect('product:order_summary')

                    else:
                        return redirect('product:order_summary') 

                else:
                    # delete user_object created when you run this view on an empty cart
                    user_object.delete()       # to be removed...
                    return redirect('product:order_summary')


    # IF USER IS NOT AUTHENTICATED................................
    else:

        # GET THE CURRENT_USER_SESSION_ID
        current_user_session_id = request.session.get('user_session_id', None)

        if current_user_session_id is None:
            print('USER DOES NOT HAVE SESSION_ID SET')
            return redirect('product:detail', slug=slug)   
        else:
            print('USER HAS A SESSION_ID')

            object, created = Product.objects.get_or_create(slug=slug)

            # session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

            session_object, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
            
            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

            if tempcart:
                current_tempcart = tempcart[0]

                if current_tempcart.items.all().filter(product__slug=object.slug):
                    current_tempcart.items.remove(session_object)
                    session_object.delete()
                    # messages.error(request, 'Item Deleted')

                    all_session_objects = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)

                    if all_session_objects:
                        return redirect('product:order_summary')  
                    else:
                        current_tempcart.delete()
                        tempcart.delete()
                        return redirect('product:order_summary')

                else:
                    return redirect('product:order_summary') 

            else:
                # delete user_object created when you run this view on an empty cart
                session_object.delete()       # to be removed...
                return redirect('product:order_summary')






# ------------------------------------------------------------------------------------
# ORDER_SUMMARY
# ------------------------------------------------------------------------------------

def order_summary(request):

    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    
    # IF USER IS AUTHENTICATED...................
    if request.user.is_authenticated:
        try:

            current_user_session_id = request.session.get('user_session_id', None)

            # cart, created = Cart.objects.get_or_create(user=request.user, ordered=False)

            # cart = Cart.objects.get(user=request.user, ordered=False)

            tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)
            
            if tempMenu:
                cart, created = Cart.objects.get_or_create(user=request.user, ordered=False)

                for police in tempMenu:
                    police.user = request.user
                    police.save()
                    cart.items.add(police)
                    cart.save()

                user_objects = cart.items.all()
                user_objects = user_objects.order_by('-added_date')
                               
                context = {
                    'objects': user_objects,
                    'cart': cart
                    }

                return render(request, 'product/order_summary.html', context)
            

            else:
                cart = Cart.objects.get(user=request.user, ordered=False)
                user_objects = cart.items.all()
                user_objects = user_objects.order_by('-added_date')       
              
                context = {
                  'objects': user_objects,
                    'cart': cart
                    }

                print('NO ITEM IN THE CART YET')
                return render(request, 'product/order_summary.html', context)
        
        except ObjectDoesNotExist:
            return redirect('product:empty_order_summary')



    # IF USER IS NOT AUTHENTICATED.................................
    else:
        try:

            current_user_session_id = request.session.get('user_session_id', None)

            tempcart = Cart.objects.get(user_session_id=current_user_session_id, ordered=False)

            if tempcart:
                session_objects = tempcart.items.all()
                session_objects = session_objects.order_by('-added_date')
            else:           
                print('NO ITEM IN THE CART YET')
                return redirect('product:empty_order_summary')

            context = {
                'objects': session_objects,
                'tempcart': tempcart
                }

            return render(request, 'product/order_summary.html', context)

        except ObjectDoesNotExist:
            return redirect('product:empty_order_summary')








# ------------------------------------------------------------------------------------
# EMPTY_ORDER_SUMMARY
# ------------------------------------------------------------------------------------
def empty_order_summary(request):

    if request.method == 'POST':
        pass
        
    else:
        return render(request, 'product/empty_order_summary.html')









# ------------------------------------------------------------------------------------
# CHECKOUT
# ------------------------------------------------------------------------------------
@login_required
def checkout(request):

    # post method
    if request.method == 'POST':
        
        form = DeliveryAddressForm(request.POST)

        if form.is_valid():
            address1 = form.cleaned_data['address1']
            address2 = form.cleaned_data['address2']
            country = form.cleaned_data['country']
            zip = form.cleaned_data['zip']
            telephone = form.cleaned_data['telephone']
            save_information = form.cleaned_data['save_information']
            payment_option = form.cleaned_data['payment_option']


            # if save_information is "True", save the form data to the delivery_address model          
            if save_information:
                delivery_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

                # if delivery_address exist, update the delivery_address, if not, create it
                if delivery_address:
                    delivery_address.address1 = address1
                    delivery_address.address2 = address2
                    delivery_address.country = country
                    delivery_address.zip = zip
                    delivery_address.telephone = telephone
                    delivery_address.save_information = save_information
                    delivery_address.payment_option = payment_option
                    
                    delivery_address.save()

                else:
                    delivery_address = DeliveryAddress.objects.create(user=request.user, address1=address1, address2=address2, country=country, zip=zip, telephone=telephone, save_information=save_information, payment_option=payment_option)

                    delivery_address.save()
            
            # But if it is not True, save the form data to the temporary_address model
            # if temporary_address exist, update it, if it does not exist, create it
            else:
                
                temporary_address, created = TemporaryAddress.objects.get_or_create(user=request.user)

                if temporary_address:
                    temporary_address.address1 = address1
                    temporary_address.address2 = address2
                    temporary_address.country = country
                    temporary_address.zip = zip
                    temporary_address.telephone = telephone
                    
                    temporary_address.save()
                
                else:
                    temporary_address = TemporaryAddress.objects.create(user=request.user, address1=address1, address2=address2, country=country, zip=zip, telephone=telephone)

                    temporary_address.save()                


            # redirect to the selected payment option page
            if payment_option == 'Stripe':
                return redirect('product:create_checkout_session')

            else:
                return redirect('product:payment_cash')


        else:
            messages.error(request, 'Form Data Not Valid')
            return redirect('product:checkout')



    # get method
    else:
        # get the previous temporary address
        temporary_address, created = TemporaryAddress.objects.get_or_create(user=request.user)
        # temporary_address.delete()      # delete the temporary address -------------------------------- TUESDAY

        # check if user has an existing delivery address and return its instance, but
        # user has no delivery address, return an empty form
        delivery_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

        if delivery_address.address1:
            form = DeliveryAddressForm(instance=delivery_address)
        else:
            form = DeliveryAddressForm()

        cart = Cart.objects.get(user=request.user, ordered=False)    

        if cart:
            user_objects = cart.items.all()
            user_objects = user_objects.order_by('-added_date')

                        
        context = {
            'form': form,
            'objects': user_objects,
            'cart': cart,
            }

        return render(request, 'product/checkout.html', context)

    




# ---------------------------------------------------------------------------------
# STRIPE CREATE CHECKOUT SESSION PAGE
# ---------------------------------------------------------------------------------
@login_required
def create_checkout_session(request):
    try:
        subject = 'TOTAL AMOUNT'
        
        cart = Cart.objects.get(user=request.user, ordered=False)
        price = cart.get_total()
        price = int(price)

        session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
                    'price_data': {'currency': 'ngn',       # ngn means Naira
                    'product_data': {'name': subject,},
                    'unit_amount': price * 100,
                    },
                    'quantity': 1,
                    }],
        
        mode='payment',
        success_url='http://127.0.0.1:8000/payment/success/',
        cancel_url='http://127.0.0.1:8000/payment/cancel/',
        )

        return redirect(session.url, code=303)
    
    except ObjectDoesNotExist:
        return redirect('product:home')

    




# ------------------------------------------------------------------------------------
# PAYMENT_CASH
# ------------------------------------------------------------------------------------
@login_required
def payment_cash(request):

    if request.method == 'POST':
        pass

    else:
        delivery_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

        temporary_address, created = TemporaryAddress.objects.get_or_create(user=request.user)

        if temporary_address.address1:
            address = temporary_address

        else:
            address = delivery_address

        context = {
            'address': address
            }

        return render(request, 'product/payment_cash.html', context)









# ------------------------------------------------------------------------------------
# SUCCESS
# ------------------------------------------------------------------------------------
@login_required
def success(request):

    try:

        # ----------------------------------------------------------------------
        # get the user_session_id
        user_session_id = request.session.get('user_session_id', None)

        if user_session_id is None:
            # create a new user_session_id
            generated_Number = random.randrange(0, 1000000)
            request.session['user_session_id'] = generated_Number
        else:
            # print the user_session_id
            print(request.session.get('user_session_id', None))
        # ----------------------------------------------------------------------


        if request.method == 'POST':
            pass

        else:

            current_user_session_id = request.session.get('user_session_id', None)

            delivery_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

            temporary_address, created = TemporaryAddress.objects.get_or_create(user=request.user)

            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)
            tempcart.delete() # delete the temporary cart

            cart = Cart.objects.filter(user=request.user, ordered=False)

            if cart:
                current_cart = cart[0]
                current_cart.ordered = True
                current_cart.save()            

                objects = current_cart.items.all()
                for object in objects:
                    object.ordered = True           
                    object.save()

            else:
                pass    
                

            
            # --------------------------------------------------------------------
            # saving the data in the cart to the Purchased model
            
            user_cart = Cart.objects.get(user=request.user, ordered=True)

            if user_cart:
                user_objects = user_cart.items.all()

                if temporary_address.address1:
                    # iterate through user_objects and save the data in the Purchased model
                    for object in user_objects:    
                        user_purchased = Purchased.objects.create(
                            user = request.user, 
                            title = object.product.title, 
                            price = object.product.price, 
                            discount = object.product.discount,
                            slug = object.product.slug,
                            description = object.product.description,
                            photo = object.product.photo,
                            quantity = object.quantity, 
                            ordered = True,               
                            receiving_address = f'{temporary_address.address1}, {temporary_address.address2}, {temporary_address.country}. Zip: {temporary_address.zip}, Telephone: {temporary_address.telephone}',
                            delivered = False,
                        )

                    user_purchased.save()

                    # delete the temporary_address
                    temporary_address.delete()      


                else:
                    # iterate through user_objects and save the data in the Purchased model
                    for object in user_objects: 
                        user_purchased = Purchased.objects.create(
                            user = request.user, 
                            title = object.product.title, 
                            price = object.product.price, 
                            discount = object.product.discount,
                            slug = object.product.slug,
                            description = object.product.description,
                            photo = object.product.photo,
                            quantity = object.quantity, 
                            ordered = True,
                            receiving_address = f'{delivery_address.address1}, {delivery_address.address2}, {delivery_address.country}. Zip: {delivery_address.zip} Telephone: {delivery_address.telephone}',
                            delivered = False,
                        )
                                        
                    user_purchased.save()

                # delete the user_cart
                user_cart.delete()

                    
            else:
                return redirect('product:home')
            # --------------------------------------------------------------------

            return render(request, 'product/success.html')
    
    except:
        return redirect('product:home')








# # ---------------------------------------------------------------------------------
# # CANCEL PAGE
# # ---------------------------------------------------------------------------------
@login_required
def cancel(request):
    if request.method == 'POST':
        pass

    else:
        return render(request, 'product/cancel.html')











# ---------------------------------------------------------------------------------
# PURCHASED
# ---------------------------------------------------------------------------------
# @login_required
# def purchased(request):
#     if request.method == 'POST':
#         pass

#     else:
#         # show all purchases made by the user
#         purchased_objects = Purchased.objects.filter(user=request.user, ordered=True)

#         purchased_objects = purchased_objects.order_by('-date_bought')

#         # purchased_objects = purchased_objects[0:5]

#         context = {'purchased_objects': purchased_objects}

#         return render(request, 'product/purchased.html', context)





@login_required
def purchased(request):
    if request.method == 'POST':
        pass

    else:
        # show all purchases made by the user
        objects = Purchased.objects.filter(user=request.user, ordered=True)

        objects = objects.order_by('-date_bought')

        # purchased_objects = purchased_objects[0:5]

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            'page_objects': page_objects,
        }

        return render(request, 'product/purchased.html', context)

   






# ---------------------------------------------------------------------------------
# SELL
# ---------------------------------------------------------------------------------
@login_required
def sell_product(request):
     
    visitor = request.user
    # allowing only special users to sell
    if visitor.username == 'rotimi':

        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                newform = form.save(commit=False)
                newform.user = request.user
                newform.save()
                return redirect('product:home')
            else:
                return redirect('product:sell_product')

        else:
            form = ProductForm()
            context = {'form': form}
            return render(request, 'product/sell_product.html', context)

    else:
        messages.error(request, 'Sorry, you are now authorized to sell on HiStore')
        return redirect('product:home')










# ---------------------------------------------------------------------------------
# UPDATE PRODUCT
# ---------------------------------------------------------------------------------
@login_required
def update_product(request, slug):

    # user = request.user

    object = Product.objects.get(slug=slug)

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            discount = form.cleaned_data['discount']
            category = form.cleaned_data['category']
            label = form.cleaned_data['label']
            description = form.cleaned_data['description']
            photo = form.cleaned_data['photo']

            object.user = request.user
            object.title = title
            object.price = price
            object.discount = discount
            object.category = category
            object.label = label
            object.description = description
            object.photo = photo

            object.save()
            return redirect('product:home')
        else:
            return redirect('product:sell_product')


    else:
        if object:
            form = ProductForm(instance=object)
        else:
            form = ProductForm()

        context = {'form': form}
        return render(request, 'product/update_product.html', context)





    
# ---------------------------------------------------------------------------------
# DELETE PRODUCT
# ---------------------------------------------------------------------------------
@login_required
def delete_product(request, slug):

    try:
        object = Product.objects.get(slug=slug)

        if object:
            object.delete()
            return redirect('product:home')
        else:
            return redirect('product:home')

    except:
        return redirect('product:home')






# ---------------------------------------------------------------------------------
# SEARCH VIEW
# ---------------------------------------------------------------------------------

def search(request):
    return render(request, 'product/search.html')





# ---------------------------------------------------------------------------------
# SEARCH VIEW
# ---------------------------------------------------------------------------------

def search_result(request):
    
    lookup_word = request.GET['lookup_word']

    if lookup_word:

        if len(lookup_word) >= 3:

            objects = Product.objects.filter(title__icontains=lookup_word) | Product.objects.filter(description__icontains=lookup_word)

            num_of_objects = objects.count()

            
            if objects:

                context = {
                'lookup_word': lookup_word,
                'objects': objects,
                'num_of_objects': num_of_objects
                }

                messages.success(request, f'Congrats, we found "{num_of_objects}" products with keyword "{lookup_word}"')
                return render(request, 'product/search_result.html', context)

            else:
                messages.error(request, f'Sorry, we presently do not have what you are looking for with "{lookup_word}"')
                return redirect('product:search')

        else:
            messages.info(request, f'There is no result for "{lookup_word}", search keyword must be atleast 3 characters long')
            return redirect('product:search')

    else:
        messages.info(request, f'You did not type any search keyword, search keyword must be atleast 3 characters long')
        return redirect('product:search')








# ---------------------------------------------------------------------------------
# MULTI-SEARCH VIEW
# ---------------------------------------------------------------------------------

def multi_search(request):
    
    # POST method
    if request.method == 'POST':
        pass

        # lookup_word = request.POST['lookup_word']

        # if lookup_word:

        #     if len(lookup_word) >= 3:

        #         objects = Product.objects.filter(title__icontains=lookup_word) | Product.objects.filter(description__icontains=lookup_word)

        #         num_of_objects = objects.count()

                
        #         if objects:

        #             context = {
        #             'lookup_word': lookup_word,
        #             'objects': objects,
        #             'num_of_objects': num_of_objects
        #             }

        #             messages.success(request, f'Congrats, we found "{num_of_objects}" products with keyword "{lookup_word}"')
        #             return render(request, 'product/search.html', context)

        #         else:
        #             messages.error(request, f'Sorry, we presently do not have what you are looking for with "{lookup_word}"')
        #             return redirect('product:search')

        #     else:
        #         messages.info(request, f'There is no result for "{lookup_word}", search keyword must be atleast 3 characters long')
        #         return redirect('product:search')

        # else:
        #     messages.info(request, f'You did not type any search keyword, search keyword must be atleast 3 characters long')
        #     return redirect('product:search')

    # GET method
    else:
        return render(request, 'product/multi_search.html')







# ---------------------------------------------------------------------------------
# CATEGORY VIEW
# ---------------------------------------------------------------------------------




    







# ---------------------------------------------------------------------------------
# COMPUTER_ELECTRONICS CATEGORY VIEW
# ---------------------------------------------------------------------------------

def computer_electronics(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Computer and Electronics")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/computer_electronics.html', context)







# ---------------------------------------------------------------------------------
# PHONES AND TABLETS CATEGORY VIEW
# ---------------------------------------------------------------------------------

def phones_tablets(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Phones and Tablets")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/phones_tablets.html', context)







# ---------------------------------------------------------------------------------
# FASHIONS AND STYLES CATEGORY VIEW
# ---------------------------------------------------------------------------------

def fashions_styles(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Fashions and Styles")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/fashions_styles.html', context)







# ---------------------------------------------------------------------------------
# HOME AND KITCHEN CATEGORY VIEW
# ---------------------------------------------------------------------------------

def home_kitchen(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Home and Kitchen")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/home_kitchen.html', context)







# ---------------------------------------------------------------------------------
# DRINKS AND WINE CATEGORY VIEW
# ---------------------------------------------------------------------------------

def drinks_wine(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Drinks and Wine")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/drinks_wine.html', context)







# ---------------------------------------------------------------------------------
# KIDS AND TOYS CATEGORY VIEW
# ---------------------------------------------------------------------------------

def kids_toys(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Kids and Toys")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/kids_toys.html', context)






# ---------------------------------------------------------------------------------
# KIDS AND TOYS CATEGORY VIEW
# ---------------------------------------------------------------------------------

def others(request):

    # POST method
    if request.method == 'POST':
        pass


    # GET method
    else:

        objects = Product.objects.filter(category__icontains="Others")

        # PAGINATION FOR FUNCTION BASED VIEW
        current_page = request.GET.get("page", 1)

        paginator = Paginator(objects, 4)       # paginate the objects after 4 items

        try:
            page_objects = paginator.page(current_page)
            
        except PageNotAnInteger:
            page_objects = paginator.page(1)

        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context = {
            # 'objects': objects,
            'page_objects': page_objects,
        }
        return render(request, 'product/others.html', context)









# ---------------------------------------------------------------------------------
# SAVE A PRODUCT FROM DETAIL PAGE VIEW
# ---------------------------------------------------------------------------------
@login_required
def save_this_product_from_detail(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    try:

        object = Product.objects.get(slug=slug)

        if SavedProduct.objects.filter(user=request.user, slug=object.slug):
            messages.error(request, f'"{object.title}" already exists in your Saved Items')
            return redirect('product:detail', slug=slug)

        else:
            user_saved_product = SavedProduct.objects.create(
                user = request.user,
                title = object.title,
                price = object.price,
                discount = object.discount,
                quantity = object.quantity,
                category = object.category,
                label = object.label,
                slug = object.slug,
                description = object.description,
                photo = object.photo,
            )
            user_saved_product.save()

            # ----------------- modifying the user_menu to "True" ------------
            user_menu, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
            
            if user_menu:
                user_menu.save_this_product = True
                user_menu.save()
            # --------------------------------------------------------------

            messages.success(request, f'"{object.title}" added to your Saved Items')
            return redirect('product:detail', slug=slug)


    except ObjectDoesNotExist:
        return redirect('product:detail', slug=slug)







# ---------------------------------------------------------------------------------
# SAVE A PRODUCT FROM ORDER SUMMARY PAGE VIEW
# ---------------------------------------------------------------------------------
@login_required
def save_this_product_from_order_summary(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    try:
        
        object = Product.objects.get(slug=slug)

        if SavedProduct.objects.filter(user=request.user, slug=object.slug):
            messages.error(request, f'"{object.title}" already exists in your Saved Items')
            return redirect('product:order_summary')

        else:
            user_saved_product = SavedProduct.objects.create(
                user = request.user,
                title = object.title,
                price = object.price,
                discount = object.discount,
                quantity = object.quantity,
                category = object.category,
                label = object.label,
                slug = object.slug,
                description = object.description,
                photo = object.photo,
            )
            user_saved_product.save()

            # ----------------- modifying the user_menu to "True" ------------
            user_menu, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
            
            if user_menu:
                user_menu.save_this_product = True
                user_menu.save()
            # --------------------------------------------------------------

            messages.success(request, f'"{object.title}" added to your Saved Items')
            return redirect('product:order_summary')


    except ObjectDoesNotExist:
        return redirect('product:order_summary')


       





# ---------------------------------------------------------------------------------
# UNSAVE A PRODUCT FROM DETAIL PAGE VIEW
# ---------------------------------------------------------------------------------
@login_required
def unsave_this_product_from_detail(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    try:
        object = Product.objects.get(slug=slug)

        saved_object = SavedProduct.objects.filter(user=request.user, slug=object.slug)
        saved_object.delete()

        # ----------------- modifying the user_menu to "False" ------------
        user_menu, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
        
        if user_menu:
            user_menu.save_this_product = False
            user_menu.save()
        # --------------------------------------------------------------

        messages.error(request, f'"{object.title}" removed from your Saved Items')
        return redirect('product:detail', slug=slug)

    except ObjectDoesNotExist:
        return redirect('product:detail', slug=slug)







# ---------------------------------------------------------------------------------
# UNSAVE A PRODUCT FROM ORDER SUMMARY PAGE VIEW
# ---------------------------------------------------------------------------------
@login_required
def unsave_this_product_from_order_summary(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    try:
        object = Product.objects.get(slug=slug)

        saved_object = SavedProduct.objects.filter(user=request.user, slug=object.slug)
        saved_object.delete()

        # ----------------- modifying the user_menu to "False" ------------
        user_menu, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)
        
        if user_menu:
            user_menu.save_this_product = False
            user_menu.save()
        # --------------------------------------------------------------

        messages.error(request, f'"{object.title}" removed from your Saved Items')
        return redirect('product:order_summary')

    except ObjectDoesNotExist:
        return redirect('product:order_summary')

    








# ---------------------------------------------------------------------------------
# SAVED ITEM VIEW
# ---------------------------------------------------------------------------------
@login_required
def savedproducts(request):
    
    user_saved_objects = SavedProduct.objects.filter(user=request.user)
    user_saved_objects = user_saved_objects.order_by('-added_date')

    context = {'user_saved_objects': user_saved_objects}
    return render(request, 'product/savedproducts.html', context)






# ---------------------------------------------------------------------------------
# UNSAVE A PRODUCT FROM SAVED PRODUCTS PAGE
# ---------------------------------------------------------------------------------
@login_required                        
def unsave_this_product_from_savedproducts(request, slug):

    # CREATE/GET USER_SESSION_ID
    # ----------------------------------------------------------------------
    # get the user_session_id
    user_session_id = request.session.get('user_session_id', None)

    if user_session_id is None:
        # create a new user_session_id
        generated_Number = random.randrange(0, 1000000)
        request.session['user_session_id'] = generated_Number
    else:
        # print the user_session_id
        print(request.session.get('user_session_id', None))
    # ----------------------------------------------------------------------
    
    try:
        object = Product.objects.get(slug=slug)

        saved_object = SavedProduct.objects.filter(user=request.user, slug=slug)
        saved_object.delete()

        # ----------------- modifying the user_menu to "False" ------------
        user_menu = Menu.objects.get(user=request.user, product=object, ordered=False)
        if user_menu:
            user_menu.save_this_product = False
            user_menu.save()
        # --------------------------------------------------------------

        messages.error(request, f'"{object.title}" removed from your Saved Items')
        return redirect('product:savedproducts')

    except ObjectDoesNotExist:
        return redirect('product:savedproducts')



