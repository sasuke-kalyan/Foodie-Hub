from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from restaurants import views as home_views
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('restaurants/', include('restaurants.urls')),
    path('menu/', include('menu.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('reviews/', include('reviews.urls')),
    path('coupons/', include('coupons.urls')),
    path('owner/', include('owner_dashboard.urls')),
    path('analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),
    path('flash-sales/', include('flash_sales.urls')),
    path('chat/', include('chat.urls')),
    path('profile/', include('profiles.urls')),
    path('rewards/', include('gamification.urls')),
    path('gallery/', include('gallery.urls')),
    path('accounts/set-language/', acc_views.set_language, name='set_language'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
