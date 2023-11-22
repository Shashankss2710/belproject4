from cProfile import Profile
from django.shortcuts import render
from cProfile import Profile
from django.shortcuts import render, redirect #import redirect 
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages, auth #this messages allow us to send error messeges 
from profileapp.models import Profile

# Create your views here.

def Settings(request):
    user_profile = Profile.objects.get(user = request.user) #first step is to get the user Profile object from our models 
    
    if request.method == 'POST':                         #this field si to update info in settings

        if request.FILES.get('image') == None:                     #if user is only updating bio and location 
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:                       #if user is updating everyhting inclung profile image
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
    
    return render(request, 'Settingsapp/settings.html', {'user_profile': user_profile}) #next step is to pass {user_profile = user_profile} the userprofile to html 
    
