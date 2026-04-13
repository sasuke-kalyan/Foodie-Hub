from django.urls import path
from . import views
app_name = 'chat'
urlpatterns = [
    path('r/<slug:restaurant_slug>/', views.chat_room, name='room'),
    path('owner/', views.owner_chat_list, name='owner_list'),
    path('owner/<int:room_id>/', views.owner_chat_room, name='owner_room'),
    path('api/<int:room_id>/messages/', views.get_messages_api, name='messages_api'),
]
