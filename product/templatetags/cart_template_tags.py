
# USING COUNT()
# =========================================================================================================================

# from django import template
# from product.models import Product, Menu, Cart


# register = template.Library()


# # FOR LOGGED IN USERS
# @register.filter
# def user_current_cart_count(request):

#     current_user_session_id = request.session.get('user_session_id', None)

#     user = request.user

#     cart = Cart.objects.filter(user=user, ordered=False) 
    
#     tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)

    
#     if cart and tempcart:
#         current_cart = cart[0]
#         return current_cart.items.count() 
#     elif cart:
#         current_cart = cart[0]
#         return current_cart.items.count()
#     elif tempcart:
#         current_tempcart = tempcart[0]
#         return current_tempcart.items.count()
#     else:       
#         return 0



                


# # FOR NOT LOGGED IN USERS
# @register.filter
# def session_current_cart_count(request):

#     current_user_session_id = request.session.get('user_session_id', None)

#     if current_user_session_id is None:
#         return 0

#     else:
#         tempcart = Cart.objects.filter(user_session_id=current_user_session_id, ordered=False)
        
#         if tempcart:
#             current_tempcart = tempcart[0]
#             return current_tempcart.items.count()
#         else:           
#             return 0







# USING QUANTITIES
# =========================================================================================================================

from django import template
from product.models import Product, Menu, Cart, Purchased, SavedProduct


register = template.Library()


#-----------------------------------------------------------------------------------------------------------------
# order_summary items count
#-----------------------------------------------------------------------------------------------------------------

# for authenticated users
# ---------------------------

@register.filter
def user_current_cart_count(request):

    current_user_session_id = request.session.get('user_session_id', None)

    user = request.user

    # cart = Menu.objects.filter(user=user, ordered=False)

    cart = Cart.objects.filter(user=user, ordered=False)
    
    tempcart = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)


    if cart:
        current_cart = cart[0]
        user_current_cart = current_cart.items.all().filter(user=request.user)

        total_qty = 0      

        for object in user_current_cart:
            total_qty = total_qty + object.quantity
        return total_qty


    elif tempcart:
        current_tempcart = tempcart[0]

        session_current_tempcart = current_tempcart.items.all().filter(user_session_id=current_user_session_id)

        total_temp_qty = 0
        for object in session_current_tempcart:
            total_temp_qty = total_temp_qty + object.quantity
        return total_temp_qty

    else:       
        return 0



                

# for unauthenticated users
# ----------------------------------

@register.filter
def session_current_cart_count(request):

    current_user_session_id = request.session.get('user_session_id', None)


    tempcart = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)
    
    if tempcart:
        total_temp_qty = 0
        for object in tempcart:
            total_temp_qty = total_temp_qty + object.quantity
        return total_temp_qty 
        
    else:           
        return 0

#-----------------------------------------------------------------------------------------------------------------







#-----------------------------------------------------------------------------------------------------------------
# purchased items count
#-----------------------------------------------------------------------------------------------------------------

@register.filter
def user_purchased_product_count(request):

    user = request.user

    user_purchased_objects = Purchased.objects.filter(user=user)

    if user_purchased_objects:
        total_qty = 0
        for object in user_purchased_objects:
            total_qty = total_qty + object.quantity
        return total_qty

    else:       
        return 0








#-----------------------------------------------------------------------------------------------------------------
# saved items count
#-----------------------------------------------------------------------------------------------------------------

@register.filter
def user_saved_product_count(request):

    user = request.user

    user_saved_objects = SavedProduct.objects.filter(user=user) 



    if user_saved_objects:
        return user_saved_objects.count()

    else:       
        return 0