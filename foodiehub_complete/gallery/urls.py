from django.urls import path
from . import views
app_name = 'gallery'
urlpatterns = [
    path('r/<slug:slug>/', views.restaurant_gallery, name='restaurant'),
]
