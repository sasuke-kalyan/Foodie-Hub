from django.db import models
from restaurants.models import Restaurant

class RestaurantPhoto(models.Model):
    PHOTO_TYPE_CHOICES = [
        ('food', 'Food Photo'),
        ('interior', 'Restaurant Interior'),
        ('exterior', 'Restaurant Exterior'),
        ('team', 'Team / Chef'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='restaurant_photos/')
    caption = models.CharField(max_length=200, blank=True)
    photo_type = models.CharField(max_length=20, choices=PHOTO_TYPE_CHOICES, default='food')
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-uploaded_at']

    def __str__(self):
        return f"{self.restaurant.name} — {self.get_photo_type_display()}"
