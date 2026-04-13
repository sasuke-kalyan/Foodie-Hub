from django.db import models
from accounts.models import User
from menu.models import MenuItem

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'menu_item')

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name}"
