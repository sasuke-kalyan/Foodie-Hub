from django.contrib import admin
from .models import Restaurant, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine_type', 'city', 'is_active', 'is_veg', 'delivery_time']
    list_filter = ['is_active', 'is_veg', 'city']
    search_fields = ['name', 'cuisine_type']
    prepopulated_fields = {'slug': ('name',)}
