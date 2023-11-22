from cProfile import Profile
from django.shortcuts import render, redirect #import redirect 
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages, auth #this messages allow us to send error messeges 
from profileapp.models import Profile


def signup(request):
#our fields in signup.html with their name attributes
    if request.method == 'POST':
        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']
        password2 =request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exits!')    #if email already in use
                return redirect('signup/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username is already taken!') #if username already exists
                return redirect('signup/')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)  #if everyhting is correct save user
                user.save()

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)      #connect our user auth with user profile info in database
                new_profile.save()
                return redirect('login/')

        else:
            messages.info(request, 'passwords do not match')     #if passwords do not match
            return redirect('signup/')


    else:
       return render(request, 'registrationapp/signup.html')






def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login/')

    else:
        return render(request, 'registrationapp/login.html')




