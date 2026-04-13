from django.db import models
from restaurants.models import Restaurant

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Starters', 'Starters'),
        ('Main Course', 'Main Course'),
        ('Snacks', 'Snacks'),
        ('Breads', 'Breads'),
        ('Desserts', 'Desserts'),
        ('Beverages', 'Beverages'),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Main Course')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_veg = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    class Meta:
        ordering = ['category', 'name']
