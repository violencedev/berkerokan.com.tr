from django.urls import path, include

from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ChangePasswordView,
    ForgotCredentialsView,
    VerifyEmailView
)

urlpatterns = [
    path("login", LoginView, name="authentication/login"),
    path("register", RegisterView, name="authentication/register"),
    path("logout", LogoutView, name="authentication/logout"),
    path("change-password", ChangePasswordView, name="authentication/change-password"),
    path('forgot-credentials', ForgotCredentialsView, name = 'authentication/forgot-credentials'),
    path('verify-email', VerifyEmailView, name = 'authentication/verify-email')
]
