from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile

class EditAccountForm(ModelForm):
    class Meta:
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': ('Kullanıcı Adı'),
            'email': ('E-Posta Adresi'),
            'first_name': ('İsim'),
            'last_name': ('Soy İsim'),
        }
        
class EditProfileForm(ModelForm):
    class Meta:
        model = UserProfile 
        fields = ('is_in_mailing_list', 'others_can_see_my_profile')
        labels = {
            'is_in_mailing_list': ('E-Posta Gönderimlerine İzin Ver'),
            'others_can_see_my_profile': ('Diğer Kullanıcıların Beni Görmesine İzin Ver'),
        }