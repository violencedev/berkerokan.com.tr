from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import EditAccountForm, EditProfileForm

# Create your views here.

def get_user_info(user):
  
  return {
    'account_id': user.id,
    'username': user.username,
    'email': user.email,
    'first_name': user.first_name,
    'last_name': user.last_name  
  } | get_user_profile_info(user)

def get_user_profile_info(user):
  
  try:
    user_profile = UserProfile.objects.get(account = user)
  except UserProfile.DoesNotExist:
    return {}
  else:
    return user_profile.__dict__

def ProfileView(request, username: str = ''):
  if username and len(username) >= 1:
    try:
      specified_user = User.objects.get(username = username)
    except User.DoesNotExist:
      return redirect('home')
    else:
      if get_profile(specified_user).others_can_see_my_profile:
        return render(request, 'profile.html', get_user_info(specified_user) | {'editable': specified_user == request.user})
      elif request.user == specified_user:
        return render(request, 'profile.html', get_user_info(specified_user) | {'editable': True})
      else:
        return redirect('home')
  elif request.user.is_authenticated:
    return render(request, 'profile.html', get_user_info(request.user) | {'editable': True})
  
def get_profile(user):
  try:
    user_profile = UserProfile.objects.get(account = user)
  except UserProfile.DoesNotExist:
    return False 
  else:
    return user_profile  

@login_required
def ProfileEditView(request):

    account_form = EditAccountForm(instance=request.user)
    profile_form = EditProfileForm(instance=get_profile(request.user))
    context = {'account_form': account_form, 'profile_form': profile_form, 'profile': get_user_info(request.user)}
    
    if request.method == 'POST':
        profile = get_profile(request.user)
        account_form = EditAccountForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=profile)
        if account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            
            if request.user.email != request.session['old_email']:
              profile.email_verified = False
              profile.save()
            
            del request.session['old_email']
            
            return redirect('self-profile')
        else: 
          return redirect('profile-edit')
    else:
        request.session['old_email'] = request.user.email
        return render(request, 'edit_account.html', context)