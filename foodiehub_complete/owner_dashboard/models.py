from django.db import models
from accounts.models import User
from restaurants.models import Restaurant

class OwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    restaurant = models.OneToOneField(Restaurant, on_delete=models.SET_NULL, null=True, blank=True, related_name='owner_profile')
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owner: {self.user.username}"
