from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q 

# Create your views here.

def LoginView(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return redirect('home')

def RegisterView(request):
    if not request.user.is_authenticated:
        return render(request, 'register.html')
    else:
        return redirect('home')


def SubmitLoginView(request):
    if request.POST and not request.user.is_authenticated:
        username, password = request.POST['username'], request.POST['password']

        user = authenticate(request, username = username, password = password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('authentication/login')
    else:
        return redirect('authentication/login')

def SubmitRegisterView(request):
    if request.POST and not request.user.is_authenticated:
        username, email, password, re_password = request.POST['username'], request.POST['email'], request.POST['password'], request.POST['re-password']


        if password == re_password and not User.objects.filter(Q(username = username) | Q(email = email)).exists():

                user = User.objects.create_user(username = username, email = email, password = password)
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return redirect('authentication/register')

    else:
        return redirect('authentication/register')

@login_required
def LogoutView(request):
    logout(request)
    return redirect('home')
