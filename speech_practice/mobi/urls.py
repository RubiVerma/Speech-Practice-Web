from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('practice/', views.practice, name='practice'),
    path('check/', views.check, name='check'),
    path('next/', views.next_sentence, name='next'),
    path('previous/', views.previous_sentence, name='previous'),
    path('progress/', views.progress, name='progress'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logged_out/', views.logged_out, name='logged_out'),
    
]
