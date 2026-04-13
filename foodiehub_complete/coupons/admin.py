from django.contrib import admin
from .models import Coupon
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_order_value', 'expiry_date', 'used_count', 'is_active']
    list_editable = ['is_active']
