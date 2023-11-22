from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from profileapp.models import Profile, FollowersCount
from django.contrib.auth.models import User
from homeapp.models import Post



@login_required(login_url='login')
def profile(request, pk): #pk
        user_object = User.objects.get(username=pk) #we are passin our user = usernamer to the url
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=pk)
        user_post_length = len(user_posts)  #we check the amount of posts here 

        follower = request.user.username
        user = pk

        if FollowersCount.objects.filter(follower=follower, user=user).first():    #this function is for the follow/unfollow button to appear 
                button_text = 'Unfollow'                                            # according to if we follow the user 
        else:                                                                       #then we pass the variables into html 
                button_text = 'Follow'


        user_followers = len(FollowersCount.objects.filter(user=pk))          #same here with followers/following count 
        user_following = len(FollowersCount.objects.filter(follower=pk))     #passing the variables and disply them in html

        context = {
                'user_object': user_object,
                'user_profile': user_profile,
                'user_posts': user_posts,
                'user_post_length': user_post_length,
                'button_text': button_text,
                'user_followers': user_followers,
                'user_following': user_following,
        }
        return render(request, 'profileapp/index.html', context)



@login_required(login_url='login')
def follow(request):
        if request.method == 'POST':
                follower = request.POST['follower']
                user = request.POST['user']

                if FollowersCount.objects.filter(follower=follower, user=user).first():
                        delete_follower = FollowersCount.objects.get(follower=follower, user=user)
                        delete_follower.delete()
                        return redirect('/profile/'+user)   #this function is user already follow user so unfollow user
                else:
                        new_follower = FollowersCount.objects.create(follower=follower, user=user)
                        new_follower.save()
                        return redirect('/profile/'+user)

        else:
                return redirect('home')

