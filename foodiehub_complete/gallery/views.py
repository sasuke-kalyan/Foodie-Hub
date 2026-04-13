from django.shortcuts import render, get_object_or_404
from restaurants.models import Restaurant
from .models import RestaurantPhoto

def restaurant_gallery(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    photos = RestaurantPhoto.objects.filter(restaurant=restaurant)
    photo_type = request.GET.get('type', '')
    if photo_type:
        photos = photos.filter(photo_type=photo_type)
    return render(request, 'gallery/restaurant_gallery.html', {
        'restaurant': restaurant,
        'photos': photos,
        'photo_type': photo_type,
        'types': RestaurantPhoto.PHOTO_TYPE_CHOICES,
    })
