from django.db import models
from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    cuisine_type = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100, default='Hyderabad')
    phone = models.CharField(max_length=15, blank=True)
    delivery_time = models.CharField(max_length=30, default='30-45 min')
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=40)
    min_order = models.DecimalField(max_digits=8, decimal_places=2, default=99)
    is_veg = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    offer_text = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(restaurant=self)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 4.0

    def review_count(self):
        from reviews.models import Review
        return Review.objects.filter(restaurant=self).count()

    def __str__(self):
        return self.name
