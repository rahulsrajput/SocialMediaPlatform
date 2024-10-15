from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, SignUpForm
from .models import Tweet, Comment, Notification
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


@login_required(login_url='login_user')
def home(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    context = {'tweets':tweets}
    return render(request, 'app/Home.html', context)


# Auth -------------------
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            login(request, user_obj)
            messages.success(request, 'login sucessfully')
            return redirect('home')
        else:
            return redirect('login_user')

    return render(request, 'auth/Login.html')



@login_required(login_url='login_user')
def logout_user(request):
    logout(request)
    messages.success(request, 'logout sucessfully')
    return redirect('login_user')



def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created sucessfully!')
            
            login(request , user)
            return redirect('home')

    form = SignUpForm()
    return render(request, 'auth/Signup.html', context={'form':form})



# Profile ----------------------------------
@login_required(login_url='login_user')
def profile(request, user):  
    # Check if the requested username is the same as the logged-in user
    if request.user.is_authenticated and request.user.username == user:
        # Use the logged-in user's profile
        user = request.user  
    else:
        # Try to fetch the user by username
        # Raises 404 if user not found
        user = get_object_or_404(User, username=user)  
    

    # Flag: If the logged-in user is viewing their own profile, you can add custom logic here
    is_own_profile = request.user == user

    # Both works similar there is no perfomance difference
    # tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    tweets = user.tweets.all().order_by('-created_at')
    
    context ={'user':user, 'is_own_profile':is_own_profile, 'tweets':tweets}
    return render(request, 'auth/Profile.html', context)



@login_required(login_url='login_user')
def edit_profile(request, user):
    user = get_object_or_404(User, username=user)

    if request.user != user:
        return redirect('profile', user=request.user.username)


    form = UserEditForm(instance=user)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated!')
            return redirect('profile', user=user.username)

    context = {'form':form}
    return render(request, 'auth/EditProfile.html', context)



# Tweet -----------------
@login_required(login_url='login_user')
def create_tweet(request):
    if request.method == "POST":
        content = request.POST.get('content')
        media = request.FILES.get('media', None)

        if content or media:
            tweet = Tweet.objects.create(
                user=request.user,
                content=content,
                media=media
            )
            
            messages.success(request, 'Tweet created sucessfully')
            return redirect('home')
        else:
            messages.error(request, 'please add some text or media')


    return render(request, 'tweet/CreateTweet.html')



@login_required(login_url='login_user')
def delete_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    
    if tweet.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this tweet.")

    tweet.delete()
    return redirect('home')



@login_required(login_url='login_user')
def edit_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    
    if tweet.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this tweet.")

    if request.method == "POST":
        content = request.POST.get("content")
        if 'media' in request.FILES:
            media = request.FILES.get("media")
        else:
            media = tweet.media

        tweet.content = content
        tweet.media = media
        tweet.save()

        messages.success(request, "tweet updated!!")
        return redirect('profile', user=request.user.username)

    context = {'tweet':tweet}
    return render(request, 'tweet/EditTweet.html',context)



# Tweet Comment view
@login_required(login_url='login_user')
def detail_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    comments = tweet.comments.all().order_by('-created_at')

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                content = content,
                tweet = tweet,
                user = request.user
            )
            return redirect('home')
        else:
            messages.error(request, 'please dont leave empty comment box')

    context = {'tweet':tweet, 'comments':comments}
    return render(request, 'tweet/DetailTweet.html', context)





# misc --------------------------------
@login_required(login_url='login_user')
def search_users(request):
    query = request.GET.get('query')
    
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    context = {'users':users}
    return render(request, 'app/Search.html', context)


@login_required(login_url='login_user')
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    if request.user not in tweet.likes.all():
        tweet.likes.add(request.user)

    Notification.objects.create(
        user = tweet.user,
        message = f'{request.user} liked your tweet - {tweet}'
    ).save()
    
    return redirect('home')


@login_required(login_url='login_user')
def unlike_tweet(request, pk):
    tweet = get_object_or_404(Tweet, pk=pk)

    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)
    
    return redirect('home')


@login_required(login_url='login_user')
def unfollow(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user in target_user.followers.all():
        request.user.following.remove(target_user)
    
    return redirect('home')


@login_required(login_url='login_user')
def follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user not in target_user.followers.all():
        request.user.following.add(target_user)

    
    Notification.objects.create(
        user = target_user,
        message = f'{request.user} Follow You'
    ).save()
    
    return redirect('home')




# Notification -------------------
@login_required(login_url='login_user')
def notifications(request):
    return render(request, 'notifications.html')


@login_required(login_url='login_user')
def notifications_fetch(request):
    notifications_list = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    notifications_count = notifications_list.count()

    notifications_data = [
        {
            'id' : notification.id,
            'message' : notification.message,
        }
        for notification in notifications_list
    ]

    return JsonResponse({
        'notifications': notifications_data,
        'count': notifications_count,
    })


@login_required(login_url='login_user')
def mark_as_read(request):
    notification = Notification.objects.filter(user=request.user)
    notification.delete()
    return redirect('notifications')



def followers(request, username):
    target_user = get_object_or_404(User, username=username)
    followers = target_user.followers.all()
    return render(request, 'auth/Follower.html', context={'followers': followers, 'target_user': target_user})

def followings(request, username):
    target_user = get_object_or_404(User, username=username)
    followings = target_user.following.all()
    return render(request, 'auth/Following.html', context={'followings': followings, 'target_user': target_user})