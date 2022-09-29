from django.urls import path, include

from .views import (
    LoginView,
    SubmitLoginView,
    LogoutView,
    RegisterView,
    SubmitRegisterView,
    ChangePasswordView,
    SubmitChangePassword,
    ForgotCredentialsView
)

urlpatterns = [
    path("login", LoginView, name="authentication/login"),
    path("submit-login", SubmitLoginView, name="authentication/login/submit"),
    path("register", RegisterView, name="authentication/register"),
    path("submit-register", SubmitRegisterView, name="authentication/register/submit"),
    path("logout", LogoutView, name="authentication/logout"),
    path("change-password", ChangePasswordView, name="authentication/change-password"),
    path(
        "submit-change-password",
        SubmitChangePassword,
        name="authentication/change-password/submit",
    ),
    path('forgot-credentials', ForgotCredentialsView, name = 'authentication/forgot-credentials')
]
