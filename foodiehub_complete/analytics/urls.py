from django.urls import path
from . import views
app_name = 'analytics'
urlpatterns = [
    path('', views.admin_analytics, name='dashboard'),
    path('map/', views.city_map_view, name='city_map'),
]
