from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from restaurants import views as home_views
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ INTRO WILL LOAD FIRST
    path('', TemplateView.as_view(template_name="intro.html")),

    # ✅ MAIN HOME PAGE
    path('home/', home_views.home, name='home'),

    # (optional) keep intro URL also
    path('intro/', TemplateView.as_view(template_name="intro.html")),

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
]

# ✅ MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)