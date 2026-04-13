from django.db import models
from accounts.models import User
from coupons.models import Coupon

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    birthday_coupon_sent = models.BooleanField(default=False)
    birthday_coupon_year = models.IntegerField(null=True, blank=True)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referred_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='referrals')
    referral_credits = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    subscription_plan = models.CharField(max_length=20, choices=[
        ('none', 'No Plan'),
        ('basic', 'Basic - ₹99/month'),
        ('premium', 'Premium - ₹199/month'),
    ], default='none')
    subscription_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.referral_code:
            import random, string
            self.referral_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    def is_birthday_today(self):
        from django.utils import timezone
        if not self.date_of_birth:
            return False
        today = timezone.now().date()
        return self.date_of_birth.day == today.day and self.date_of_birth.month == today.month

    def subscription_active(self):
        from django.utils import timezone
        if self.subscription_plan == 'none':
            return False
        return self.subscription_expiry and self.subscription_expiry >= timezone.now().date()
