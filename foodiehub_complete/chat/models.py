from django.db import models
from accounts.models import User
from restaurants.models import Restaurant

class ChatRoom(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='chat_rooms')
    order_id = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('customer', 'restaurant')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.username} ↔ {self.restaurant.name}"

    def unread_count_for_customer(self):
        return self.messages.filter(is_read=False, sender_type='owner').count()

    def unread_count_for_owner(self):
        return self.messages.filter(is_read=False, sender_type='customer').count()

    def last_message(self):
        return self.messages.last()


class ChatMessage(models.Model):
    SENDER_CHOICES = [('customer', 'Customer'), ('owner', 'Restaurant Owner')]
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:40]}"
