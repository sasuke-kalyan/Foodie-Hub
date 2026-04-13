from django.db import models

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [('flat', 'Flat'), ('percent', 'Percentage')]
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='flat')
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    max_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    expiry_date = models.DateField()
    usage_limit = models.IntegerField(default=100)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        from django.utils import timezone
        return self.is_active and self.expiry_date >= timezone.now().date() and self.used_count < self.usage_limit
