from django.db import models
from accounts.models import User

class Notification(models.Model):
    TYPE_CHOICES = [
        ('order_placed', 'Order Placed'),
        ('order_preparing', 'Order Preparing'),
        ('order_out', 'Out for Delivery'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('coupon', 'New Coupon'),
        ('promo', 'Promotion'),
        ('general', 'General'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='general')
    order_id = models.CharField(max_length=20, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
