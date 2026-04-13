from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from restaurants.models import Restaurant
from menu.models import MenuItem
from orders.models import Order, OrderItem
from .models import OwnerProfile

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'owner':
            messages.error(request, "Access denied. Owner account required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

@login_required
@owner_required
def dashboard(request):
    try:
        profile = request.user.owner_profile
        restaurant = profile.restaurant
    except:
        restaurant = None

    today = timezone.now().date()
    context = {'restaurant': restaurant}

    if restaurant:
        today_orders = Order.objects.filter(
            items__restaurant_name=restaurant.name,
            created_at__date=today
        ).distinct()
        pending_orders = Order.objects.filter(
            items__restaurant_name=restaurant.name,
            status__in=['placed', 'preparing']
        ).distinct()
        completed_orders = Order.objects.filter(
            items__restaurant_name=restaurant.name,
            status='delivered'
        ).distinct()
        menu_count = MenuItem.objects.filter(restaurant=restaurant).count()
        today_revenue = sum(o.total_price for o in today_orders if o.status != 'cancelled')
        context.update({
            'today_orders': today_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'menu_count': menu_count,
            'today_revenue': today_revenue,
        })
    return render(request, 'owner_dashboard/dashboard.html', context)

@login_required
@owner_required
def manage_menu(request):
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        restaurant = None
    items = MenuItem.objects.filter(restaurant=restaurant) if restaurant else []
    return render(request, 'owner_dashboard/menu.html', {'items': items, 'restaurant': restaurant})

@login_required
@owner_required
def add_menu_item(request):
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        messages.error(request, "No restaurant linked to your account.")
        return redirect('owner_dashboard:dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_veg = request.POST.get('is_veg') == 'on'
        is_bestseller = request.POST.get('is_bestseller') == 'on'
        image = request.FILES.get('image')
        MenuItem.objects.create(
            restaurant=restaurant, name=name, category=category,
            description=description, price=price, is_veg=is_veg,
            is_bestseller=is_bestseller, image=image
        )
        messages.success(request, "Menu item added!")
        return redirect('owner_dashboard:menu')
    return render(request, 'owner_dashboard/add_item.html', {'restaurant': restaurant})

@login_required
@owner_required
def edit_menu_item(request, item_id):
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        return redirect('owner_dashboard:dashboard')
    item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    if request.method == 'POST':
        item.name = request.POST.get('name', item.name)
        item.category = request.POST.get('category', item.category)
        item.description = request.POST.get('description', item.description)
        item.price = request.POST.get('price', item.price)
        item.is_veg = request.POST.get('is_veg') == 'on'
        item.is_available = request.POST.get('is_available') == 'on'
        item.is_bestseller = request.POST.get('is_bestseller') == 'on'
        if request.FILES.get('image'):
            item.image = request.FILES['image']
        item.save()
        messages.success(request, "Item updated!")
        return redirect('owner_dashboard:menu')
    return render(request, 'owner_dashboard/edit_item.html', {'item': item})

@login_required
@owner_required
def delete_menu_item(request, item_id):
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        return redirect('owner_dashboard:dashboard')
    item = get_object_or_404(MenuItem, id=item_id, restaurant=restaurant)
    item.delete()
    messages.success(request, "Item deleted.")
    return redirect('owner_dashboard:menu')

@login_required
@owner_required
def manage_orders(request):
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        restaurant = None
    orders = []
    if restaurant:
        order_ids = OrderItem.objects.filter(restaurant_name=restaurant.name).values_list('order_id', flat=True).distinct()
        orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
    return render(request, 'owner_dashboard/orders.html', {'orders': orders, 'restaurant': restaurant})

@login_required
@owner_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f"Order status updated to {order.get_status_display()}")
    return redirect('owner_dashboard:orders')
# Add this to owner_dashboard/views.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from restaurants.models import Restaurant
from django.utils import timezone
import json

@login_required
def toggle_restaurant_status(request, restaurant_id):
    """One-click open/close toggle"""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    try:
        if request.user.owner_profile.restaurant != restaurant:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
    except:
        return JsonResponse({'error': 'No restaurant linked'}, status=403)

    restaurant.is_active = not restaurant.is_active
    restaurant.save()
    status = "opened" if restaurant.is_active else "closed"
    messages.success(request, f"Restaurant {status} successfully!")
    return redirect('owner_dashboard:dashboard')


@login_required
def set_auto_close(request):
    """Set a time for restaurant to auto-close"""
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        messages.error(request, "No restaurant linked.")
        return redirect('owner_dashboard:dashboard')

    if request.method == 'POST':
        close_time = request.POST.get('auto_close_time', '')
        open_time = request.POST.get('auto_open_time', '')
        # Store in session for demo (in production use a model field)
        request.session['auto_close_time'] = close_time
        request.session['auto_open_time'] = open_time
        messages.success(request, f"Auto-schedule set! Closes at {close_time}, Opens at {open_time}")
        return redirect('owner_dashboard:dashboard')

    return redirect('owner_dashboard:dashboard')


@login_required
def check_auto_close(request):
    """API endpoint — check if restaurant should auto close now"""
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        return JsonResponse({'status': 'error'})

    now = timezone.localtime(timezone.now())
    current_time = now.strftime('%H:%M')
    close_time = request.session.get('auto_close_time', '')
    open_time = request.session.get('auto_open_time', '')

    action = None
    if close_time and current_time >= close_time and restaurant.is_active:
        restaurant.is_active = False
        restaurant.save()
        action = 'closed'
    elif open_time and current_time >= open_time and not restaurant.is_active:
        restaurant.is_active = True
        restaurant.save()
        action = 'opened'

    return JsonResponse({
        'is_active': restaurant.is_active,
        'action': action,
        'current_time': current_time,
    })
