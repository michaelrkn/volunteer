from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('friends', views.friends, name='friends'),
    # path('outvote', views.outvote, name='outvote'),
    path('page/<str:urlSlug>', views.page, name='page'),
]