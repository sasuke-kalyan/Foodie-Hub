from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DeliveryAddress


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('FoodieHub Info', {'fields': ('role', 'phone', 'profile_picture')}),
    )


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'pincode', 'is_default']
    list_filter = ['city', 'is_default']
