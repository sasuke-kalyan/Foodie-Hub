from django.shortcuts import render
from .models import Coupon
from django.utils import timezone

def coupon_list(request):
    coupons = Coupon.objects.filter(is_active=True, expiry_date__gte=timezone.now().date())
    return render(request, 'coupons/list.html', {'coupons': coupons})
