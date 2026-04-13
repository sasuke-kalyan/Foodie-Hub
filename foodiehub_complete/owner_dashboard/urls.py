from django.urls import path
from . import views
app_name = 'owner_dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('menu/', views.manage_menu, name='menu'),
    path('menu/add/', views.add_menu_item, name='add_item'),
    path('menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_item'),
    path('menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_item'),
    path('orders/', views.manage_orders, name='orders'),
    path('orders/update/<int:order_id>/', views.update_order_status, name='update_order'),
    path('restaurant/toggle/<int:restaurant_id>/', views.toggle_restaurant_status, name='toggle_status'),
    path('restaurant/auto-close/', views.set_auto_close, name='set_auto_close'),
    path('restaurant/check-close/', views.check_auto_close, name='check_auto_close'),
]
