from email.mime import image
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from profileapp.models import  FollowersCount, Profile
from django.contrib.auth.models import User

from profileapp.views import follow, profile
from .models import Post, LikePost
from itertools import chain
import random


@login_required(login_url='login')
def Home(request):
        user_object = User.objects.get(username=request.user.username)          #this 2 lines help us import our user data in the home..
        user_profile =Profile.objects.get(user=user_object)                     # html so userdata is display like profile pic, username
       




        user_following_list = []      #this make the user only see posts of users he follows   filter() this functions loops through our objects in our database                                                            
        feed = []
        user_following = FollowersCount.objects.filter(follower=request.user.username)
        for users in user_following:
            user_following_list.append(users.user)
        for usernames in user_following_list:
            feed_lists = Post.objects.filter(user=usernames)
            feed.append(feed_lists)
        feed_list = list(chain(*feed))

        
        #user suggestion algotithm (only suggest people that doesnt follow u and refresh list everytime u refresh page. only show five users in template)
        all_users = User.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = User.objects.get(username=user.user)
            user_following_all.append(user_list)

        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = User.objects.filter(username=request.user.username)
        final_suggestions_list = [ x for x in list(new_suggestions_list) if ( x not in list(current_user) )]
        random.shuffle(final_suggestions_list)

        username_profile = []         
        username_profile_list = []

        for users in final_suggestions_list:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        suggestions_username_profile_list = list(chain(*username_profile_list))
        
       

        posts = Post.objects.all() #we were are importing the user posts feed to the home page so we can see them
        return render(request, 'homeapp/home.html', {'user_profile': user_profile, 'posts': posts, 'suggestions_username_profile_list': suggestions_username_profile_list[:4] }) #change posts to feed_list if we wanna see posts of people we follow

                                                                                     #important as fuck





@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/login')






#upload function to upload posts to our database 

@login_required(login_url='login')
def upload(request):

        if request.method == 'POST':
            user = request.user.username
            image = request.FILES.get('image_upload') 
            caption = request.POST['caption'] #[] when we upload text

            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()

            return redirect('home')
        else:
           return redirect('home')







@login_required(login_url='login')
def like_post(request):
        username = request.user.username #we we get the username of the current login username 
        post_id = request.GET.get('post_id') #we get the id of the post

        post = Post.objects.get(id=post_id) #we get the post object 

        like_filter = LikePost.objects.filter(post_id=post_id, username=username).first() #we check if the post has alredy been like for us  #we can user filter() if object no exists 'likes
        
        if like_filter == None:
            new_like =LikePost.objects.create(post_id=post_id, username=username)
            new_like.save()
            post.likes = post.likes+1 
            post.save()
            return redirect('home')

        else: 
            like_filter.delete()
            post.likes = post.likes-1
            post.save()
            return redirect('home') 



def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
           profile_lists = Profile.objects.filter(id_user=ids)
           username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list)) 

    return render(request, 'homeapp/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})
    