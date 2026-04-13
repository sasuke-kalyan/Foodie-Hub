from django.contrib import admin
from .models import FlashSale

@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu_item', 'discount_percent', 'start_time', 'end_time', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
