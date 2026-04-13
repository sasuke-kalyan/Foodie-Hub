import json
import hmac
import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from coupons.models import Coupon
from accounts.models import DeliveryAddress
from django.conf import settings

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('menu_item').all()
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:view')

    coupon = None
    discount = 0
    coupon_code = request.session.get('coupon_code', '')
    subtotal = cart.get_total()
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiry_date__gte=timezone.now().date())
            if subtotal >= coupon.min_order_value:
                if coupon.discount_type == 'flat':
                    discount = coupon.discount_value
                else:
                    discount = (subtotal * coupon.discount_value) / 100
                if coupon.max_discount:
                    discount = min(discount, coupon.max_discount)
        except Coupon.DoesNotExist:
            pass

    delivery_charge = 40
    final_total = subtotal + delivery_charge - discount
    addresses = DeliveryAddress.objects.filter(user=request.user)
    google_maps_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    razorpay_key = getattr(settings, 'RAZORPAY_KEY_ID', '')

    context = {
        'cart': cart, 'items': items, 'subtotal': subtotal,
        'discount': discount, 'delivery_charge': delivery_charge,
        'final_total': final_total, 'coupon': coupon,
        'addresses': addresses, 'google_maps_key': google_maps_key,
        'razorpay_key': razorpay_key,
        'final_total_paise': int(final_total * 100),
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def create_razorpay_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    try:
        import razorpay
        cart = Cart.objects.get(user=request.user)
        subtotal = cart.get_total()
        delivery_charge = 40
        discount = 0
        coupon_code = request.session.get('coupon_code', '')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiry_date__gte=timezone.now().date())
                if subtotal >= coupon.min_order_value:
                    if coupon.discount_type == 'flat':
                        discount = coupon.discount_value
                    else:
                        discount = (subtotal * coupon.discount_value) / 100
                    if coupon.max_discount:
                        discount = min(discount, coupon.max_discount)
            except Coupon.DoesNotExist:
                pass

        final_total = subtotal + delivery_charge - discount
        amount_paise = int(final_total * 100)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'payment_capture': 1,
        })
        return JsonResponse({
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': request.user.phone,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def razorpay_callback(request):
    if request.method == 'POST':
        data = request.POST
        try:
            key_secret = settings.RAZORPAY_KEY_SECRET
            generated_signature = hmac.new(
                key_secret.encode(),
                f"{data['razorpay_order_id']}|{data['razorpay_payment_id']}".encode(),
                hashlib.sha256
            ).hexdigest()
            if generated_signature == data['razorpay_signature']:
                request.session['razorpay_payment_id'] = data['razorpay_payment_id']
                request.session['razorpay_order_id'] = data['razorpay_order_id']
                request.session['payment_verified'] = True
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'error': 'Signature mismatch'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=500)


@login_required
def place_order(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('menu_item').all()
    if not items.exists():
        messages.error(request, "Cart is empty.")
        return redirect('cart:view')

    delivery_address = request.POST.get('delivery_address', '').strip()
    phone = request.POST.get('phone', request.user.phone)
    payment_method = request.POST.get('payment_method', 'cod')
    special_instructions = request.POST.get('special_instructions', '')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')

    if not delivery_address:
        messages.error(request, "Please enter a delivery address.")
        return redirect('orders:checkout')

    subtotal = cart.get_total()
    delivery_charge = 40
    discount = 0
    coupon_code = request.session.get('coupon_code', '')
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiry_date__gte=timezone.now().date())
            if subtotal >= coupon.min_order_value:
                if coupon.discount_type == 'flat':
                    discount = coupon.discount_value
                else:
                    discount = (subtotal * coupon.discount_value) / 100
                if coupon.max_discount:
                    discount = min(discount, coupon.max_discount)
                coupon.used_count += 1
                coupon.save()
        except Coupon.DoesNotExist:
            pass

    final_total = subtotal + delivery_charge - discount
    order = Order.objects.create(
        user=request.user,
        delivery_address=delivery_address,
        phone=phone,
        payment_method=payment_method,
        subtotal=subtotal,
        delivery_charge=delivery_charge,
        discount=discount,
        total_price=final_total,
        coupon_code=coupon_code,
        special_instructions=special_instructions,
        razorpay_payment_id=razorpay_payment_id,
        is_paid=bool(razorpay_payment_id),
    )

    for cart_item in items:
        OrderItem.objects.create(
            order=order,
            menu_item=cart_item.menu_item,
            item_name=cart_item.menu_item.name,
            item_price=cart_item.menu_item.price,
            quantity=cart_item.quantity,
            restaurant_name=cart_item.menu_item.restaurant.name,
        )

    cart.items.all().delete()
    request.session.pop('coupon_code', None)
    request.session.pop('razorpay_payment_id', None)
    request.session.pop('payment_verified', None)
    messages.success(request, f"Order placed! Order ID: {order.order_id}")
    return redirect('orders:confirmation', order_id=order.order_id)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/confirmation.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    status_steps = ['placed', 'preparing', 'out_for_delivery', 'delivered']
    current_index = status_steps.index(order.status) if order.status in status_steps else 0
    return render(request, 'orders/tracking.html', {
        'order': order,
        'status_steps': status_steps,
        'current_index': current_index,
    })


@login_required
def export_orders_excel(request):
    if not request.user.is_staff:
        return redirect('home')
    import csv
    from django.http import HttpResponse
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="foodiehub_orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Email', 'Phone', 'Items', 'Subtotal', 'Delivery', 'Discount', 'Total', 'Payment', 'Status', 'Date'])
    orders = Order.objects.all().order_by('-created_at')
    for order in orders:
        items_str = '; '.join([f"{i.item_name} x{i.quantity}" for i in order.items.all()])
        writer.writerow([
            order.order_id, order.user.username, order.user.email,
            order.phone, items_str, order.subtotal, order.delivery_charge,
            order.discount, order.total_price, order.get_payment_method_display(),
            order.get_status_display(), order.created_at.strftime('%d-%m-%Y %H:%M'),
        ])
    return response

@login_required
def order_receipt(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/receipt.html', {'order': order})
