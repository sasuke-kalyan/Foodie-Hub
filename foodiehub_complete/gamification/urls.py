from django.urls import path
from . import views
app_name = 'gamification'
urlpatterns = [
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('rewards/', views.my_rewards, name='rewards'),
]
