from django.shortcuts import render
from django.utils import timezone
from .models import FlashSale
from django.http import JsonResponse

def flash_sale_list(request):
    now = timezone.now()
    active_sales = FlashSale.objects.filter(is_active=True, start_time__lte=now, end_time__gte=now)
    upcoming = FlashSale.objects.filter(is_active=True, start_time__gt=now).order_by('start_time')[:3]
    return render(request, 'flash_sales/list.html', {
        'active_sales': active_sales,
        'upcoming': upcoming,
    })

def flash_sale_timer_api(request, pk):
    try:
        sale = FlashSale.objects.get(pk=pk)
        return JsonResponse({
            'seconds_remaining': sale.time_remaining_seconds(),
            'is_live': sale.is_live(),
        })
    except FlashSale.DoesNotExist:
        return JsonResponse({'seconds_remaining': 0, 'is_live': False})
