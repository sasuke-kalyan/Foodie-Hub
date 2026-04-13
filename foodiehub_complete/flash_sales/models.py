from django.db import models
from menu.models import MenuItem

class FlashSale(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='flash_sales', null=True, blank=True)
    discount_percent = models.PositiveIntegerField(default=20, help_text="Discount percentage (e.g. 20 for 20%)")
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    banner_color = models.CharField(max_length=7, default='#ff4444')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_live(self):
        from django.utils import timezone
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

    def time_remaining_seconds(self):
        from django.utils import timezone
        now = timezone.now()
        if now > self.end_time:
            return 0
        return int((self.end_time - now).total_seconds())

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']
