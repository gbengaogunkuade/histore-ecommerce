from django.shortcuts import render, redirect
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.





#---------------------------------------------------------------------------------------------------------------------
# REGISTER PAGE
#---------------------------------------------------------------------------------------------------------------------

def visitor_register(request):

    if request.method == 'POST':

        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        verify_email = request.POST['verify_email']
        password = request.POST['password']
        verify_password = request.POST['verify_password']


        visitor = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)                # THIS CREATES THE NEW USER ACCOUNT

        visitor.set_password(visitor.password) # THIS CHANGES THE PLAIN TEXT PASSWORD TO A "HASHED PASSWORD"

        visitor.is_active = True    # THIS SETS THE USER AS AN ACTIVE USER

        visitor.save()

        messages.success(request, f'Dear {first_name}, your registration was successful, your username is {username}!')
        return redirect('login')


    else:
        return render(request, 'visitor/register.html')





# def visitor_register(request):

#     if request.method == 'POST':

#         form = RegisterForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             verify_email = form.cleaned_data['verify_email']
#             password = form.cleaned_data['password']
#             verify_password = form.cleaned_data['verify_password']

#             visitor = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

#             visitor.set_password(visitor.password) # CHANGE THE PLAIN TEXT PASSWORD TO A "HASHED PASSWORD"

#             visitor.is_active = True    # SET THE USER AS AN ACTIVE USER

#             visitor.save()

#             messages.success(request, f'Dear {first_name}, your registration was successful, your username is {username}!')
#             return redirect('login')

#         else:
#             # messages.error(request, 'INVALID DATA DETECTED!')
#             return redirect('register')



#     else:

#         form = RegisterForm(request.POST)

#         context = {'form': form}

#         return render(request, 'visitor/register.html', context)










#---------------------------------------------------------------------------------------------------------------------
# LOGIN PAGE
#---------------------------------------------------------------------------------------------------------------------

def visitor_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']


        visitor = authenticate(request, username=username, password=password)       # THIS AUTHENTICATES THE USER

        if visitor:
            if visitor.is_active:               # THIS CHECKS IF USER IS STILL ACTIVE
                login(request, visitor)
                messages.success(request, 'You are now logged in!')
                return redirect('shop:home')

        
        else:
            messages.error(request, 'You are not a registered member of this site, please register and try again')
            return redirect('login')


    else:

        return render(request, 'visitor/login.html')








#---------------------------------------------------------------------------------------------------------------------
# LOGIN_TO_CONTINUE PAGE
#---------------------------------------------------------------------------------------------------------------------

# def visitor_login_to_continue(request):

#     if request.method == 'POST':

#         username = request.POST['username']
#         password = request.POST['password']


#         visitor = authenticate(request, username=username, password=password)       # THIS AUTHENTICATES THE USER

#         if visitor:
#             if visitor.is_active:               # THIS CHECKS IF USER IS STILL ACTIVE
#                 login(request, visitor)

#                 if 'next' in request.POST:
#                     messages.success(request, 'You are redirected to the requested page!')
#                     return redirect(request.POST['next'])
#                 else:
#                     messages.success(request, 'You are now logged in!')
#                     return redirect('shop:home')
        
#         else:
#             messages.error(request, 'You are not a registered member of this site, please register and try again')
#             return redirect('login')


#     else:

#         return render(request, 'visitor/login_to_continue.html')




def visitor_login_to_continue(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        next = request.POST['next']             # GET "next" FROM request.POST


        visitor = authenticate(request, username=username, password=password)       # THIS AUTHENTICATES THE USER

        if visitor:
            if visitor.is_active:               # THIS CHECKS IF USER IS STILL ACTIVE
                login(request, visitor)

                if next:                        # IF "next" EXISTS IN "requests.POST"
                    messages.success(request, 'You are redirected to the requested page!')
                    return redirect(next)       # RETURN THE VALUE OF "next"
                else:
                    messages.success(request, 'You are now logged in!')
                    return redirect('shop:home')
        
        else:
            messages.error(request, 'You are not a registered member of this site, please register and try again')
            return redirect('login')


    else:

        return render(request, 'visitor/login_to_continue.html')













#---------------------------------------------------------------------------------------------------------------------
# LOGOUT PAGE
#---------------------------------------------------------------------------------------------------------------------

@login_required
def visitor_logout(request):

    visitor = request.user.first_name

    logout(request)         # THIS LOGS OUT THE CURRENT USER
    messages.success(request, f'Dear, {visitor}, you are now logout!')
    return redirect('login')







