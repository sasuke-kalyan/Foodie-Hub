from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from orders.models import Order, OrderItem
from accounts.models import User
from restaurants.models import Restaurant
from menu.models import MenuItem
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

@login_required
def admin_analytics(request):
    if not request.user.is_staff:
        return redirect('home')

    total_users = User.objects.filter(role='customer').count()
    total_owners = User.objects.filter(role='owner').count()
    total_restaurants = Restaurant.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_price'))['total'] or 0

    # Top selling items
    top_items = OrderItem.objects.values('item_name', 'restaurant_name').annotate(
        total_ordered=Sum('quantity')).order_by('-total_ordered')[:10]

    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:20]

    # Order status counts
    delivered_count = Order.objects.filter(status='delivered').count()
    preparing_count = Order.objects.filter(status='preparing').count()
    placed_count = Order.objects.filter(status='placed').count()
    cancelled_count = Order.objects.filter(status='cancelled').count()

    # Monthly revenue (last 6 months)
    monthly_labels = []
    monthly_revenue = []
    for i in range(5, -1, -1):
        d = timezone.now() - timedelta(days=i * 30)
        label = d.strftime('%b')
        rev = Order.objects.filter(
            status='delivered',
            created_at__year=d.year,
            created_at__month=d.month
        ).aggregate(total=Sum('total_price'))['total'] or 0
        monthly_labels.append(label)
        monthly_revenue.append(float(rev))

    # Top restaurants
    top_rests = OrderItem.objects.values('restaurant_name').annotate(
        total=Count('id')).order_by('-total')[:5]
    top_restaurant_names = [r['restaurant_name'] for r in top_rests]
    top_restaurant_orders = [r['total'] for r in top_rests]

    import json
    context = {
        'total_users': total_users,
        'total_owners': total_owners,
        'total_restaurants': total_restaurants,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'top_items': top_items,
        'recent_orders': recent_orders,
        'delivered_count': delivered_count,
        'preparing_count': preparing_count,
        'placed_count': placed_count,
        'cancelled_count': cancelled_count,
        'monthly_labels': json.dumps(monthly_labels),
        'monthly_revenue': json.dumps(monthly_revenue),
        'top_restaurant_names': json.dumps(top_restaurant_names),
        'top_restaurant_orders': json.dumps(top_restaurant_orders),
    }
    return render(request, 'analytics/dashboard.html', context)


@login_required
def city_map_view(request):
    if not request.user.is_staff:
        return redirect('home')
    city = request.GET.get('city', '')
    restaurants = Restaurant.objects.all()
    if city:
        restaurants = restaurants.filter(city__icontains=city)
    cities = Restaurant.objects.values_list('city', flat=True).distinct()
    return render(request, 'analytics/city_map.html', {
        'restaurants': restaurants,
        'cities': cities,
        'city': city,
        'google_maps_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    })
