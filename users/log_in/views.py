from django.shortcuts import render
from log_in.forms import UserForm, UserProfileInfoForm
# these imports are for the login process
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'log_in/index.html')

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user #this sets up the onetoone relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form =UserProfileInfoForm()

    return render(request, 'log_in/register.html', {'user_form':user_form,
                                                    'profile_form':profile_form,
                                                    'registered':registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("failed login attempt")
            print('Username: {} and password {}'.format(username,password))
            return HttpResponse("INVALID LOGIN DETAILS")
    else:
        return render(request, 'log_in/login.html',{})

@login_required
def appstore(request):
    return HttpResponse("You are logged in, welcome to the secret pages")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))