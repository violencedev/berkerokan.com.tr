
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail

import random
import hashlib

# Create your views here.


def LoginView(request):
    print(request.session["remember_me"])
    if not request.user.is_authenticated:
        try:
            request.session["remember_me"]
        except KeyError:
            request.session["remember_me"] = {
                "username": "",
                "password": "",
                "checked": "",
            }

        print(request.session["remember_me"])

        return render(request, "login.html", request.session["remember_me"])
    else:
        return redirect("home")


def RegisterView(request):
    if not request.user.is_authenticated:
        return render(request, "register.html")
    else:
        return redirect("home")


@login_required
def ChangePasswordView(request):
    form = PasswordChangeForm(request.user)
    return render(request, "change-password.html", {"form": form})


def ForgotCredentialsView(request):
  if not request.user.is_authenticated:
    try:
      request.session['recovery_code']
    except KeyError:
      request.session['recovery_code'] = False
    if request.method == 'POST':

        if request.session['recovery_code']:
          code = request.POST['recovery-code']
          code_hashed = hashlib.md5(str(code).encode()).hexdigest()
          
          if code_hashed == request.session['recovery_code']:
            messages.success(request, 'Hesabınıza yeni bir şifre belirleyin lütfen')
            del request.session['recovery_code']
            
            return render(request, 'forgot-credentials.html', {'change_allowed': True})
          else:
            messages.error(request, 'Kod hatalı')
          
          return redirect('authentication/forgot-credentials')

        try:
          request.POST['password']
          request.POST['re-password']
        except KeyError:
          pass 
        else:
          password, re_password = request.POST['password'], request.POST['re-password']
          
          if password == re_password:
            
            try:
              user = User.objects.get(email = request.session['recovery_email'])
            except User.DoesNotExist:
              messages.error(request, 'Nedeni Bilinmeyen Hata: (KOD: 1-001). Yöneticilere başvurunuz')
              return redirect('authentication/forgot-credentials')
            else:
              if user.password != password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Hesabınızın şifresi başarıyla değiştirildi')
                
                del request.session['recovery_email']
                
                return redirect('home')
              else:
                messages.error(request, 'Son şifrenizi yeni şifre olarak kullanamazsınız')
                return redirect('authentication/forgot-credentials')
          else:
            messages.error(request, 'Şifreler farklı!')
            return redirect('authentication/forgot-credentials')
        
        email = request.POST['email']
        
        try:
          user = User.objects.get(email = email)
        except User.DoesNotExist:
          return redirect('authentication/forgot-credentials')
        
        else:
          recovery_code = str(random.randint(100000, 999999))
          
          request.session['recovery_code'] = hashlib.md5(recovery_code.encode()).hexdigest()
          request.session['recovery_email'] = email
          
          messages.info(request, f'E-Posta adresine kurtarma kodu gönderildi: ({email})')
          send_mail('berkerokan.com.tr - Hesap Kurtarma İşlemi', f'Birisi hesabınıza kayıtlı bu eposta adresini kullanarak hesap kurtarma işlemi başlattı. \nEğer bunu yapan siz değilseniz güvenli bir şekilde maili silebilirsiniz. \n\nKurtarma Kodu: {recovery_code}', 'furkanesen1900@gmail.com', [email])
          
          return redirect('authentication/forgot-credentials')
    else:
      return render(request, 'forgot-credentials.html', {'recovery_code': request.session['recovery_code']})
  else:
    return redirect('home')

def SubmitLoginView(request):
    if request.POST and not request.user.is_authenticated:
        username, password = (
            request.POST["username"],
            request.POST["password"],
        )

        try:
            remember_me_status = request.POST["remember-me"]
        except KeyError:
            remember_me_status = False
        else:
            remember_me_status = True

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if remember_me_status:
                request.session["remember_me"] = {
                    "username": username,
                    "password": password,
                    "checked": "checked",
                }
            else:
                del request.session["remember_me"]

            return redirect("home")
        else:
            return redirect("authentication/login")
    else:
        return redirect("authentication/login")


def SubmitRegisterView(request):
    if request.POST and not request.user.is_authenticated:
        username, email, password, re_password = (
            request.POST["username"],
            request.POST["email"],
            request.POST["password"],
            request.POST["re-password"],
        )

        if (
            password == re_password
            and not User.objects.filter(Q(username=username) | Q(email=email)).exists()
        ):

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("home")
        else:
            return redirect("authentication/register")

    else:
        return redirect("authentication/register")


def SubmitChangePassword(request):
    if request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("home")
        else:
            return redirect("authentication/change-password")
    else:
        return redirect("authentication/change-password")


@login_required
def LogoutView(request):
    try:
        saved_data = request.session["remember_me"]
    except KeyError:
        saved_data = {"username": "", "password": "", "checked": ""}

    logout(request)

    request.session["remember_me"] = saved_data
    return redirect("home")
