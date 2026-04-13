from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from menu.models import MenuItem
from coupons.models import Coupon
from django.utils import timezone

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('menu_item__restaurant').all()
    coupon = None
    discount = 0
    coupon_code = request.session.get('coupon_code', '')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiry_date__gte=timezone.now().date())
            subtotal = cart.get_total()
            if subtotal >= coupon.min_order_value:
                if coupon.discount_type == 'flat':
                    discount = coupon.discount_value
                else:
                    discount = (subtotal * coupon.discount_value) / 100
                discount = min(discount, coupon.max_discount) if coupon.max_discount else discount
        except Coupon.DoesNotExist:
            request.session.pop('coupon_code', None)

    subtotal = cart.get_total()
    delivery_charge = 40 if subtotal > 0 else 0
    final_total = subtotal + delivery_charge - discount
    context = {
        'cart': cart, 'items': items, 'subtotal': subtotal,
        'discount': discount, 'delivery_charge': delivery_charge,
        'final_total': final_total, 'coupon': coupon,
    }
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{menu_item.name} added to cart!")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok', 'count': cart.get_item_count()})
    return redirect(request.META.get('HTTP_REFERER', 'cart:view'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart:view')

@login_required
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart:view')

@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(code=code, is_active=True, expiry_date__gte=timezone.now().date())
            cart = Cart.objects.get(user=request.user)
            if cart.get_total() < coupon.min_order_value:
                messages.error(request, f"Minimum order ₹{coupon.min_order_value} required.")
            else:
                request.session['coupon_code'] = code
                messages.success(request, f"Coupon '{code}' applied!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon.")
    return redirect('cart:view')

@login_required
def remove_coupon(request):
    request.session.pop('coupon_code', None)
    messages.info(request, "Coupon removed.")
    return redirect('cart:view')
