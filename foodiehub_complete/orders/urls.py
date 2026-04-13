from django.urls import path
from . import views
app_name = 'orders'
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place/', views.place_order, name='place'),
    path('razorpay/create/', views.create_razorpay_order, name='razorpay_create'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
    path('confirmation/<str:order_id>/', views.order_confirmation, name='confirmation'),
    path('history/', views.order_history, name='history'),
    path('tracking/<str:order_id>/', views.order_tracking, name='tracking'),
    path('export/excel/', views.export_orders_excel, name='export_excel'),
]
