from django.urls import path
from . import views
app_name = 'reviews'
urlpatterns = [
    path('add/<slug:restaurant_slug>/', views.add_review, name='add'),
    path('delete/<int:review_id>/', views.delete_review, name='delete'),
]
