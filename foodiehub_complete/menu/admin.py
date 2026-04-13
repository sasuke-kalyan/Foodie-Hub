from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_veg', 'is_available', 'is_bestseller']
    list_filter = ['category', 'is_veg', 'is_available', 'is_bestseller', 'restaurant']
    search_fields = ['name', 'restaurant__name']
    list_editable = ['is_available', 'is_bestseller']
