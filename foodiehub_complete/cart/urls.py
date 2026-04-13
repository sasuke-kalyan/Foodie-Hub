from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
    path('', views.cart_view, name='view'),
    path('add/<int:item_id>/', views.add_to_cart, name='add'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    path('update/<int:item_id>/', views.update_quantity, name='update'),
    path('coupon/apply/', views.apply_coupon, name='apply_coupon'),
    path('coupon/remove/', views.remove_coupon, name='remove_coupon'),
]
