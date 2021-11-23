from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from visitor.forms import RegisterForm, LoginForm, UserProfileForm, UserAddressForm

from product.models import Product, Menu, Cart, DeliveryAddress, TemporaryAddress, Purchased
from product.forms import ProductForm, DeliveryAddressForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives        # for sending instant mails





# Create your views here.





#---------------------------------------------------------------------------------------------------------------------
# REGISTER VIEW
#---------------------------------------------------------------------------------------------------------------------

def visitor_register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            verify_email = form.cleaned_data['verify_email']
            password = form.cleaned_data['password']
            verify_password = form.cleaned_data['verify_password']

            taken_user = User.objects.filter(username=username)

            taken_email = User.objects.filter(email=email)

            if taken_user:
                messages.info(request, 'Username Taken! Please Use Another Username')
                print('username is taken')
                return render(request, 'registration/register.html', {'form': RegisterForm()})
            elif taken_email:
                messages.info(request, 'Email Taken! Please Use Another Email')
                print('email is taken')
                return render(request, 'registration/register.html', {'form': RegisterForm()})
            else:
                if password == verify_password and email == verify_email:
                    new_visitor = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)                # THIS CREATES THE NEW USER ACCOUNT

                    new_visitor.set_password(new_visitor.password) # THIS CHANGES THE PLAIN TEXT PASSWORD TO A "HASHED PASSWORD"

                    new_visitor.is_active = True    # THIS SETS THE USER AS AN ACTIVE USER

                    new_visitor.save()

                    messages.success(request, f'Dear {first_name}, registration successful!, your username is {username}!')
                    return redirect('login')

                else:
                    return redirect('register')


        else:
            print('invalid data submitted')
            form = RegisterForm(request.POST)
            context = {'form': form}
            return render(request, 'registration/register.html', context)
        

    else:
        form = RegisterForm(request.POST)
        context = {'form': form}
        return render(request, 'registration/register.html', context)







#---------------------------------------------------------------------------------------------------------------------
# LOGIN VIEW
#---------------------------------------------------------------------------------------------------------------------

def visitor_login(request):

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

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            visitor = authenticate(request, username=username, password=password)       # THIS AUTHENTICATES THE USER

            if visitor:
                if visitor.is_active:               # THIS CHECKS IF USER IS STILL ACTIVE
                    login(request, visitor)
                    messages.success(request, 'You are now logged in!')

                    
                    # IF USER IS AUTHENTICATED...................
                    if request.user.is_authenticated:
                        try:

                            current_user_session_id = request.session.get('user_session_id', None)

                            tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)
                            
                            if tempMenu:
                                cart, created = Cart.objects.get_or_create(user=request.user, ordered=False)

                                for police in tempMenu:
                                    police.user = request.user
                                    police.save()
                                    cart.items.add(police)
                                    cart.save()

                                return redirect('product:home')
                            

                            else:
                                cart = Cart.objects.get(user=request.user, ordered=False)
                                return redirect('product:home')
                            
                            
                        
                        except ObjectDoesNotExist:
                            return redirect('product:home')
                    

                    else:
                        messages.error(request, 'You are not logged in')
                        return redirect('login') 

                else:
                    messages.error(request, 'Your account is no longer active on this site, contact site administrator')
                    return redirect('login')

            else:
                messages.error(request, 'You are not a registered member of this site, please register and try again')
                return redirect('register')
        
        else:
            messages.error(request, 'Invalid Data Submitted!')
            return redirect('login')


    # GET method
    else:

        form = LoginForm(request.POST)
        context = {'form': form}
        return render(request, 'registration/login.html', context)





    














#---------------------------------------------------------------------------------------------------------------------
# LOGIN_TO_CONTINUE VIEW 
#---------------------------------------------------------------------------------------------------------------------

def visitor_login_to_continue(request):

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

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            next = request.POST['next']            # get "next" from request.POST       

            visitor = authenticate(request, username=username, password=password)       # THIS AUTHENTICATES THE USER

            if visitor:
                if visitor.is_active:               # THIS CHECKS IF USER IS STILL ACTIVE
                    login(request, visitor)

                    if next:                                # IF "next" EXISTS IN "request.POST"
                        messages.success(request, 'You are redirected to the requested page!')

                        # IF USER IS AUTHENTICATED...................
                        if request.user.is_authenticated:
                            try:

                                current_user_session_id = request.session.get('user_session_id', None)

                                tempMenu = Menu.objects.filter(user_session_id=current_user_session_id, ordered=False)
                                
                                if tempMenu:
                                    cart, created = Cart.objects.get_or_create(user=request.user, ordered=False)

                                    for police in tempMenu:
                                        police.user = request.user
                                        police.save()
                                        cart.items.add(police)
                                        cart.save()
                                    return redirect(next)               # RETURN THE VALUE OF "next"                             

                                else:
                                    cart = Cart.objects.get(user=request.user, ordered=False)
                                    return redirect(next)               # RETURN THE VALUE OF "next"

                            except ObjectDoesNotExist:
                                return redirect(next)
                        

                        else:
                            messages.error(request, 'You are not logged in')
                            return redirect('login')

                    else:
                        pass

                else:
                    messages.error(request, 'Your account is no longer active on this site, contact site administrator')
                    return redirect('register')

            else:
                messages.error(request, 'You are not a registered member of this site, please register and try again')
                return redirect('register')

        else:
            messages.error(request, 'Invalid Data Submitted!')
            return redirect('login_to_continue')
        

    # GET method
    else:
        form = LoginForm(request.POST)
        context = {'form': form}
        return render(request, 'registration/login_to_continue.html', context)






#---------------------------------------------------------------------------------------------------------------------
# LOGOUT VIEW
#---------------------------------------------------------------------------------------------------------------------

# @login_required
def visitor_logout(request):

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

    visitor = request.user.first_name

    logout(request)         # THIS LOGS OUT THE CURRENT USER
    # messages.success(request, f'Dear, {visitor}, you are now logout!')
    return redirect('login')
    # return redirect('product:home')












#---------------------------------------------------------------------------------------------------------------------
# PROFILE VIEW
#---------------------------------------------------------------------------------------------------------------------

def visitor_profile(request):

    # POST method
    if request.method == 'POST':

        user_answer = request.POST['user_answer']           # logic user result
        user_answer = int(user_answer)

        register_form = UserProfileForm(request.POST)
        delivery_form = UserAddressForm(request.POST)

        logic_answer = request.POST['logic_answer']
        logic_answer = int(logic_answer)

        if user_answer == logic_answer:

            if register_form.is_valid() and delivery_form.is_valid():

                new_username = register_form.cleaned_data['new_username']
                first_name = register_form.cleaned_data['first_name']
                last_name = register_form.cleaned_data['last_name']
                email = register_form.cleaned_data['email']

                address1 = delivery_form.cleaned_data['address1']
                address2 = delivery_form.cleaned_data['address2']
                country = delivery_form.cleaned_data['country']
                zip = delivery_form.cleaned_data['zip']
                telephone = delivery_form.cleaned_data['telephone']

                user_detail, created = User.objects.get_or_create(username=request.user)

                if user_detail:
                    if new_username:
                        user_detail.username = new_username
                    else:
                        pass
                    user_detail.first_name = first_name
                    user_detail.last_name = last_name
                    user_detail.email = email
                    user_detail.save()
                else:
                    pass

                user_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

                if user_address:
                    user_address.user = request.user
                    user_address.address1 = address1
                    user_address.address2 = address2
                    user_address.country = country
                    user_address.zip = zip
                    user_address.telephone = telephone  
                    user_address.save()
                    messages.success(request, 'Profile updated')
                    return redirect('profile')

                else:
                    if new_username:
                        user_address = DeliveryAddress.objects.create(user=new_username, address1=address1, address2=address2, country=country, zip=zip, telephone=telephone)
                        user_address.save()

                    else:
                        user_address = DeliveryAddress.objects.create(user=request.user, address1=address1, address2=address2, country=country, zip=zip, telephone=telephone)
                        user_address.save()

                    messages.success(request, 'Profile updated')
                    return redirect('profile')

        else:
            messages.error(request, 'Wrong Answer, Try Again')
            return redirect('profile')
        

    
    # GET method
    else:
        
        first_Number = random.randrange(1, 50)
        second_Number = random.randrange(11, 45)
        logic_answer = first_Number + second_Number

        user_detail, created = User.objects.get_or_create(username=request.user)

        user_address, created = DeliveryAddress.objects.get_or_create(user=request.user)

        if user_detail and user_address.address1:
            register_form = UserProfileForm(instance=user_detail)
            delivery_form = UserAddressForm(instance=user_address)

        elif user_detail:
            register_form = UserProfileForm(instance=user_detail)
            delivery_form = UserAddressForm()

        else:
            register_form = UserProfileForm()
            delivery_form = UserAddressForm()

        context = {
            'register_form': register_form,
            'delivery_form': delivery_form,
            'logic_answer': logic_answer,
            'first_Number': first_Number,
            'second_Number': second_Number,
        }
        return render(request, 'registration/profile.html', context)






# PASSWORD CHANGE
@login_required
def visitor_password_change(request):

    form = PasswordChangeForm(request.user)

    context = {'form': form}

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated successfully!')
            return redirect('logout')
        else:
            messages.warning(request, 'Unmatched password submitted, correct and retry')


    return render(request, 'registration/password_change.html', context)






# # --------------------------------------------SENDING INSTANT MAILS ------------------------------------------

    # # ------------------------------------------
    # # sending advanced mails without attachment
    # # ------------------------------------------
    # email = EmailMessage(
    #     'Hello',                                                              # subject
    #     f'Dear {currentUser}, you have been successfully logged out.',        # message
    #     'ownerbig@freeshop.com',                                              # from
    #     [currentUserEmail, 'to2@example.com'],                                # recipients
    #     ['bcc@example.com'],                                                  # bcc
    # reply_to=['myowner@example.com'],                  
    # headers={'Message-ID': 'foo'},
    # )

    # # sending the mail
    # email.send(fail_silently=False)
    # # ------------------------------------------

    # return redirect('freeshop_login')




    # # ------------------------------------------
    # # sending advanced mails with attachment
    # # ------------------------------------------
    # email = EmailMessage(
    #     'Subject, LOGOUT successful',                                       # subject
    #     f'Dear {currentUser}, you have been successfully logged out.',      # message
    #     'ownerbig@freeshop.com',                                            # from
    #     [currentUserEmail, 'to2@example.com'],                              # recipients
    #     ['bcc@example.com'],                                                # bcc
    # reply_to=['myowner@example.com'],
    # headers={'Message-ID': 'foo'},
    # )

    # # attaching file to the mail
    # from pathlib import Path
    # photo = Path('C:\\Users\\GBENGA\\Pictures\\IBADAN.jpg')
    # email.attach_file(photo)

    # # sending the mail
    # email.send(fail_silently=False)
    # # ------------------------------------------

    # return redirect('freeshop_login')





    # # ------------------------------------------
    # # sending advanced mails in HTML format
    # # ------------------------------------------
    # subject, from_email, to = 'Subject, LOGOUT successful', 'admin@freeshop.com', currentUserEmail
    # text_content = f'Dear {currentUser}, you have been successfully logged out.'
    # html_content = f'Dear <span style="color:green; font-weight:bold;">{currentUser}</span>, <br>You have been successfully logged out.<br>Kind regards,'
    # # html_content = '<div style="background-color:yellow; height:200px; font-size:20px; padding:10px 5px 10px 5px;">Dear User, your logout from Freeshop was successful. Thanks for visiting, we hope to see you back here soon.<br><br>Kind regards,<br>Gbenga Ogunkuade<br>CEO Freeshop</div>'

    # email = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # email.attach_alternative(html_content, "text/html")

    # # attaching file to the mail
    # from pathlib import Path
    # photo = Path('C:\\Users\\GBENGA\\Pictures\\IBADAN.jpg')
    # email.attach_file(photo)

    # # sending the mail
    # email.send(fail_silently=False)
    # # ------------------------------------------

    # return redirect('freeshop_login')




# # --------------------------------------------------------------------------------------------------------------
# # EXAMPLE
# # --------------------------------------------------------------------------------------------------------------

# LOGOUT
# @login_required
# def testing_logout(request):
#     currentUser = request.user.first_name      # ASSIGNING THE CURRENT LOGGED IN USER TO "currentUser" VARIABLE
#     currentUserEmail = request.user.email

#     logout(request)
#     messages.success(request, f'Dear {currentUser}, You Have Been Successfully Logged Out!')


#     # ------------------------------------------
#     # sending simple mails
#     # ------------------------------------------
#     send_mail(
#         'MY LOGOUT MAIL',                                                   # subject
#         f'Dear {currentUser}, you have been successfully logged out.',      # message
#         'owner@freeshop.com',                                               # from
#         [currentUserEmail],                                                 # recipient
#         fail_silently=False,
#         )
#     # # ------------------------------------------

#     return redirect('testing_login')
