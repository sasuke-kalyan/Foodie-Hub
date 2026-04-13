from django.urls import path
from . import views
app_name = 'flash_sales'
urlpatterns = [
    path('', views.flash_sale_list, name='list'),
    path('timer/<int:pk>/', views.flash_sale_timer_api, name='timer'),
]
