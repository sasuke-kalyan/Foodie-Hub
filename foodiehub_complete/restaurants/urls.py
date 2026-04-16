from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.restaurant_list, name='list'),
    path('search/', views.search_view, name='search'),

    path('live-search/', views.live_search, name='live_search'),

    path('<slug:slug>/', views.restaurant_detail, name='detail'),
]