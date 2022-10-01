from django.urls import path, re_path, include

from .views import HomePageView

urlpatterns = [
    path('', HomePageView, name = 'home'),
    re_path(r'^authentication/', include('authentication.urls'), name = 'authentication'),
    re_path(r'^profile/', include('user.urls'), name = 'profile')
]
