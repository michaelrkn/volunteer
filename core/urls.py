from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('join/<str:referrer>', views.join, name='join'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('friends', views.friends, name='friends'),
    path('update', views.update, name='update'),
    path('actions', views.actions, name='actions'),
    path('actblue', views.actblue, name='actblue'),
    path('page/<str:urlSlug>', views.page, name='page'),
]