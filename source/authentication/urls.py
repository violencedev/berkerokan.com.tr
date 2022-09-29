from django.urls import path, include

from .views import LoginView, SubmitLoginView, LogoutView, RegisterView, SubmitRegisterView

urlpatterns = [
    path('login', LoginView, name = 'authentication/login'),
    path('submit-login', SubmitLoginView, name = 'authentication/login/submit'),
    path('register', RegisterView, name = 'authentication/register'),
    path('submit-register', SubmitRegisterView, name = 'authentication/register/submit'),
    path('logout', LogoutView, name = 'authentication/logout'),
]
