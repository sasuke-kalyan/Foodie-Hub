from django.urls import path
from . import views
app_name = 'profiles'
urlpatterns = [
    path('', views.my_profile_extra, name='extra'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('birthday/', views.update_birthday, name='birthday'),
    path('ref/<str:ref_code>/', views.register_with_referral, name='referral'),
]
