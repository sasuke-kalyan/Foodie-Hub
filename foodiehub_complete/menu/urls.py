from django.urls import path
from . import views
app_name = 'menu'
urlpatterns = [
    path('<slug:restaurant_slug>/', views.menu_detail, name='detail'),
]
