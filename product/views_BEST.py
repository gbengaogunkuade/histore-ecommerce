from django.shortcuts import render, redirect
from product.models import Product, Menu, Cart
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







# # ------------------------------------------------------------------------------------
# # DETAIL
# # ------------------------------------------------------------------------------------

# def detailview(request, slug):

#     # CREATING SESSION ID FOR THE USER 
#     # ---------------------------------------------------------------------
#     # get the user_session_id
#     user_session_id = request.session.get('user_session_id', None)

#     if user_session_id is None:
#         # create a new user_session_id
#         user_session_id = random.randrange(0, 1000000)
#         request.session['user_session_id'] = user_session_id
#         print('NEW USER_SESSION_ID SET')
#         print(request.session.get('user_session_id', None))
        
#     else:
#         # print the user_session_id
#         print(request.session.get('user_session_id', None))
#     # ----------------------------------------------------------------------
    
#     object, created = Product.objects.get_or_create(slug=slug)

#     context = {
#         'wording': 'THIS IS THE CONTACT PAGE',
#         'object': object,
#     }
#     return render(request,'product/detail.html', context)









# ------------------------------------------------------------------------------------
# DETAIL
# ------------------------------------------------------------------------------------

def detailview(request, slug):

    # POST STATEMENT BELOW........................
    if request.method == 'POST':

        # IF USER IS AUTHENTICATED........
        if request.user.is_authenticated:

            # get the user_session_id
            user_session_id = request.session.get('user_session_id', None)

            if user_session_id is None:
                # create a new user_session_id
                user_session_id = random.randrange(0, 1000000)
                request.session['user_session_id'] = user_session_id
            else:
                # print the user_session_id
                print(request.session.get('user_session_id', None))


            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            object, created = Product.objects.get_or_create(slug=slug)

            user_product, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)

            quantity = request.POST['form_quantity']
            quantity = int(quantity)

            if quantity >= 1:

                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    curent_cart = cart[0]

                    if curent_cart.items.all().filter(product__slug=object.slug):
                        user_product.quantity += quantity
                        user_product.save()
                    else:
                        user_product.quantity = quantity
                        user_product.save()
                        curent_cart.items.add(user_product)
                        curent_cart.save()

                else:
                    today_date = timezone.now()
                    user_product.quantity = quantity
                    user_product.save()
                    newcart = Cart.objects.create(user=request.user, created_date=today_date)
                    newcart.items.add(user_product)

                    tempMenu = Menu.objects.filter(user_session_id=current_user_session_id)

                    if tempMenu:
                        for police in tempMenu:
                            newcart.items.add(police)
                    newcart.save()

            else:
                print('INVALID QUANTITY')
                return redirect('product:detailview', slug=slug)



        # IF USER IS NOT AUTHENTICATED ........
        else:
            
            # get the user_session_id
            user_session_id = request.session.get('user_session_id', None)

            if user_session_id is None:
                # create a new user_session_id
                user_session_id = random.randrange(0, 1000000)
                request.session['user_session_id'] = user_session_id
            else:
                # print the user_session_id
                print(request.session.get('user_session_id', None))


            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            object, created = Product.objects.get_or_create(slug=slug)

            session_product, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

            quantity = request.POST['form_quantity']
            quantity = int(quantity)

            if quantity >= 1:

                tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

                if tempcart:
                    curent_tempcart = tempcart[0]

                    if curent_tempcart.items.all().filter(product__slug=object.slug):
                        session_product.quantity += quantity
                        session_product.save()
                    else:
                        session_product.quantity = quantity
                        session_product.save()
                        curent_tempcart.items.add(session_product)
                        curent_tempcart.save()

                else:
                    today_date = timezone.now()
                    session_product.quantity = quantity
                    session_product.save()
                    newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
                    newtempcart.items.add(session_product)
                    newtempcart.save()
            else:
                print('INVALID QUANTITY')
                return redirect('product:detailview', slug=slug)


        
        return redirect('product:detail', slug=slug)


    # GET STATEMENT BELOW........................
    else:
        # CREATING SESSION ID FOR THE USER 
        # ---------------------------------------------------------------------
        # get the user_session_id
        user_session_id = request.session.get('user_session_id', None)

        if user_session_id is None:
            # create a new user_session_id
            user_session_id = random.randrange(0, 1000000)
            request.session['user_session_id'] = user_session_id   
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

     
# ---------------------------------------------------------------------------------------

























# # ------------------------------------------------------------------------------------
# # ADD SINGLE ITEM TO CART
# # ------------------------------------------------------------------------------------

# def add_single_item_to_cart(request, slug):
    
#     # GET THE CURRENT_USER_SESSION_ID

#     current_user_session_id = request.session.get('user_session_id', None)

#     if current_user_session_id is None:
#         print('USER DOES NOT HAVE SESSION_ID SET')
#         return redirect('product:detail', slug=slug)   

#     else:
#         print('USER HAS A SESSION_ID')
#         object, created = Product.objects.get_or_create(slug=slug)

#         user_product, created = TempMenu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
        
#         cart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)
        
#         if cart:

#             current_cart = cart[0]

#             if current_cart.items.all().filter(product__slug=object.slug):
#                 user_product.quantity += 1
#                 user_product.save()
#                 return redirect('product:detail', slug=slug)
#             else:
#                 current_cart.items.add(user_product)    
#                 current_cart.save()
#                 return redirect('product:detail', slug=slug)
#         else:
#             today_date = timezone.now()
#             new_cart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
#             new_cart.items.add(user_product)   
#             new_cart.save()
#             return redirect('product:detail', slug=slug)









# ------------------------------------------------------------------------------------
# ADD SINGLE ITEM TO CART
# ------------------------------------------------------------------------------------

def add_single_item_to_cart(request, slug):

    # IF USER IS AUTHENTICATED........
    if request.user.is_authenticated:
        
            # GET THE CURRENT_USER_SESSION_ID
            current_user_session_id = request.session.get('user_session_id', None)

            if current_user_session_id is None:
                print('USER DOES NOT HAVE SESSION_ID SET')
                return redirect('product:detail', slug=slug)   
            else:
                print('USER HAS A SESSION_ID')

                object, created = Product.objects.get_or_create(slug=slug)

                user_product, created = Menu.objects.get_or_create(user=request.user, product=object, ordered=False)

                cart = Cart.objects.filter(user=request.user, ordered=False)

                if cart:
                    curent_cart = cart[0]

                    if curent_cart.items.all().filter(product__slug=object.slug):
                        user_product.quantity += 1
                        user_product.save()
                    else:
                        curent_cart.items.add(user_product)
                        curent_cart.save()

                else:
                    today_date = timezone.now()
                    newcart = Cart.objects.create(user=request.user, created_date=today_date)
                    newcart.items.add(user_product)

                    # tempMenu = Menu.objects.filter(user_session_id=current_user_session_id)

                    # if tempMenu:
                    #     for police in tempMenu:
                    #         newcart.items.add(police)

                    newcart.save()

            return redirect('product:detail', slug=slug)



    # IF USER IS NOT AUTHENTICATED........
    else:

        # GET THE CURRENT_USER_SESSION_ID
        current_user_session_id = request.session.get('user_session_id', None)

        if current_user_session_id is None:
            print('USER DOES NOT HAVE SESSION_ID SET')
            return redirect('product:detail', slug=slug)   

        else:
            print('USER HAS A SESSION_ID')

            object, created = Product.objects.get_or_create(slug=slug)

            session_product, created = Menu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)


            # ATTENDING TO TEMPCART
            if tempcart:
                curent_tempcart = tempcart[0]

                if curent_tempcart.items.all().filter(product__slug=object.slug):
                    session_product.quantity += 1		
                    session_product.save()
                else:
                    curent_tempcart.items.add(session_product)
                    curent_tempcart.save()

            else:
                today_date = timezone.now()
                newtempcart = Cart.objects.create(user_session_id=current_user_session_id, created_date=today_date)
                newtempcart.items.add(session_product)
                newtempcart.save()

        return redirect('product:detail', slug=slug)

      

# ---------------------------------------------------------------------------------------













# ------------------------------------------------------------------------------------
# REMOVE SINGLE ITEM FROM CART
# ------------------------------------------------------------------------------------

def remove_single_item_from_cart(request, slug):
    pass
    
#     # GET tTHE CURRENT_USER_SESSION_ID

#     current_user_session_id = request.session.get('user_session_id', None)

#     if current_user_session_id is None:
#         print('USER DOES NOT HAVE SESSION_ID SET')
#         return redirect('product:detail', slug=slug)   

#     else:
#         print('USER HAS A SESSION_ID')
#         object, created = Product.objects.get_or_create(slug=slug)

#         session_product, created = TempMenu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)
        
#         tempcart = TempCart.objects.filter(user_session_id=current_user_session_id, ordered=False)
        
#         if tempcart:

#             current_tempcart = tempcart[0]

#             if current_tempcart.items.all().filter(product__slug=object.slug):
#                 if session_product.quantity > 1:
#                     session_product.quantity -= 1
#                     session_product.save()
#                     return redirect('product:detail', slug=slug)
#                 else:
#                     current_tempcart.items.remove(session_product)
#                     session_product.delete()

#                     all_user_products = TempMenu.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                     if all_user_products:
#                         # return to order_summary
#                         return redirect('product:detail', slug=slug) 
#                     else:
#                         tempcart.delete()
#                         return redirect('product:home')  
#             else:
#                 return redirect('product:home')
#         else:
#             # delete user_product created when you run this view on an empty cart
#             session_product.delete()       # to be removed...
#             return redirect('product:home')





# ------------------------------------------------------------------------------------
# REMOVE ALL ITEMS FROM CART
# ------------------------------------------------------------------------------------

def remove_items_from_cart(request, slug):
    pass

#     current_user_session_id = request.session.get('user_session_id', None)

#     if current_user_session_id is None:
#         print('USER DOES NOT HAVE SESSION_ID SET')
#         return redirect('product:detail', slug=slug)

#     else:
#         print('USER HAS A SESSION ID')
#         object, created = Product.objects.get_or_create(slug=slug)

#         session_product, created = TempMenu.objects.get_or_create(user_session_id=current_user_session_id, product=object, ordered=False)

#         tempcart = TempCart.objects.filter(user_session_id=current_user_session_id, ordered=False)

#         if tempcart:
#             current_tempcart = tempcart[0]

#             if current_tempcart.items.all().filter(product__slug=object.slug):
#                 current_tempcart.items.remove(session_product)
#                 session_product.delete()

#                 all_user_products = TempMenu.objects.filter(user_session_id=current_user_session_id, ordered=False)

#                 if all_user_products:
#                     # return to order_summary
#                     return redirect('product:detail', slug=slug) 
#                 else:
#                     tempcart.delete()
#                     return redirect('product:home') 
                        
#             else:
#                 return redirect('product:detail', slug=slug)

#         else:
#             # delete user_product created when you run this view on an empty cart
#             session_product.delete()       # to be removed...
#             return redirect('product:home')
            






# ------------------------------------------------------------------------------------
# ORDER_SUMMARY
# ------------------------------------------------------------------------------------

def order_summary(request):

    current_user_session_id = request.session.get('user_session_id', None)

    # IF USER IS AUTHENTICATED.................................
    if request.user.is_authenticated:
        
        cart = Cart.objects.filter(user=request.user, ordered=False)

        tempMenu = Menu.objects.filter(user_session_id=current_user_session_id)

        if cart:
            current_cart = cart[0]
            if tempMenu:
                for police in tempMenu:
                    current_cart.items.add(police)
                current_cart.save()

            objects = current_cart.items.all()
            objects = objects.order_by('-added_date')

        else:           
            tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

            if tempcart:
                current_tempcart = tempcart[0]               
                objects = current_tempcart.items.all()
                objects = objects.order_by('-added_date')

        context = {
            'objects': objects
            }

        return render(request, 'product/order_summary.html', context)



    # IF USER IS NOT AUTHENTICATED.................................
    else:

        tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

        if tempcart:
            current_tempcart = tempcart[0]
            objects = current_tempcart.items.all()
            objects = objects.order_by('-added_date')
        else:           
            print('NO ITEM IN THE CART YET')
            return redirect('product:home')

        context = {
            'objects': objects
            }

        return render(request, 'product/order_summary.html', context)










