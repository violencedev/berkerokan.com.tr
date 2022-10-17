from django.urls import path, re_path, include

from .views import HomePageView, WorksView

urlpatterns = [
    path('', HomePageView, name = 'home'),
    re_path(r'^authentication/', include('authentication.urls'), name = 'authentication'),
    re_path(r'^profile/', include('user.urls'), name = 'profile'),
    re_path(r'^works/(?P<work_type>.*)', WorksView, name = 'works'), 
]
