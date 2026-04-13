from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'referral_code', 'referral_credits', 'subscription_plan', 'subscription_expiry']
    search_fields = ['user__username', 'referral_code']
    list_filter = ['subscription_plan']
