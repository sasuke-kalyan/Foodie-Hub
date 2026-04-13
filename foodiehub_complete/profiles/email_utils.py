from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order):
    try:
        subject = f"FoodieHub Order Confirmed! #{order.order_id}"
        items_text = "\n".join([
            f"  • {item.item_name} x{item.quantity} — ₹{item.get_subtotal()}"
            for item in order.items.all()
        ])
        message = f"""
Hi {order.user.username}! 🍽️

Your order has been placed successfully!

Order ID: #{order.order_id}
Items:
{items_text}

Subtotal: ₹{order.subtotal}
Delivery: ₹{order.delivery_charge}
{'Discount: -₹' + str(order.discount) if order.discount > 0 else ''}
Total Paid: ₹{order.total_price}

Delivery Address: {order.delivery_address}
Payment: {order.get_payment_method_display()}

Track your order: http://127.0.0.1:8000/orders/tracking/{order.order_id}/

Thank you for ordering with FoodieHub! ❤️
Team FoodieHub
"""
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email error: {e}")


def send_status_update_email(order):
    status_messages = {
        'preparing': "👨‍🍳 Your order is being prepared!",
        'out_for_delivery': "🛵 Your order is out for delivery!",
        'delivered': "✅ Your order has been delivered!",
        'cancelled': "❌ Your order has been cancelled.",
    }
    if order.status not in status_messages:
        return
    try:
        subject = f"FoodieHub Order Update — #{order.order_id}"
        message = f"""
Hi {order.user.username}!

{status_messages[order.status]}

Order ID: #{order.order_id}
Status: {order.get_status_display()}

Track: http://127.0.0.1:8000/orders/tracking/{order.order_id}/

Team FoodieHub ❤️
"""
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Email error: {e}")


def send_birthday_email(user, coupon_code):
    try:
        subject = f"🎂 Happy Birthday {user.username}! Here's your special gift!"
        message = f"""
🎉 Happy Birthday, {user.username}!

On this special day, we have a gift for you!

🎁 Birthday Coupon Code: {coupon_code}
✅ 30% OFF on your next order
⏰ Valid today only!

Use it at checkout and enjoy your favourite food!

With love,
Team FoodieHub 🍕🍔🍜
"""
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception as e:
        print(f"Birthday email error: {e}")
