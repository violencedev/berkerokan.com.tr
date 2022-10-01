from django.contrib.auth.models import User 
from django.db import models

# Create your models here.

class UserProfile(models.Model):
  account = models.OneToOneField(User, on_delete=models.CASCADE)
  
  email_verified = models.BooleanField(default=False)
  is_in_mailing_list = models.BooleanField(default=False)
  others_can_see_my_profile = models.BooleanField(default=True)