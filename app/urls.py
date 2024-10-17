from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    # Auth
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views.signup_user, name='signup_user'),

    # Profile
    path('<str:user>', views.profile, name='profile'),
    path('edit/<str:user>', views.edit_profile, name='edit_profile'),
    path('followers/<str:username>/', views.followers, name='followers'),
    path('followings/<str:username>/', views.followings, name='followings'),

    # Tweet
    path('createTweet/', views.create_tweet, name='create_tweet'),
    path('deleteTweet/<int:pk>', views.delete_tweet, name='delete_tweet'),
    path('editTweet/<int:pk>', views.edit_tweet, name='edit_tweet'),
    path('detailTweet/<int:pk>', views.detail_tweet, name='detail_tweet'),

    # Misc
    path('search/', views.search_users, name='search_users'),
    path('like_tweet/<int:pk>', views.like_tweet, name='like_tweet'),
    path('unlike_tweet/<int:pk>', views.unlike_tweet, name='unlike_tweet'),

    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),


    # Notification
    path('notifications/', views.notifications, name='notifications'),
    path('notifications_fetch/', views.notifications_fetch, name='notifications_fetch'),
    path('notifications/mark-as-read/', views.mark_as_read, name='mark_as_read'),   

    # path("test/", views.test, name='test')
]