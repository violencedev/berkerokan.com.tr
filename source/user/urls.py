
from django.urls import path, re_path

from .views import ProfileView, ProfileEditView

urlpatterns = [
    path('', ProfileView, name = 'self-profile'),
    path('edit', ProfileEditView, name = 'profile-edit'),
    re_path(r'(?P<username>.*)', ProfileView, name = 'profile'),
]
