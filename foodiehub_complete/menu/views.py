from django.shortcuts import render, get_object_or_404
from .models import MenuItem
from restaurants.models import Restaurant

def menu_detail(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    categories = items.values_list('category', flat=True).distinct()
    context = {'restaurant': restaurant, 'items': items, 'categories': categories}
    return render(request, 'menu/menu.html', context)
