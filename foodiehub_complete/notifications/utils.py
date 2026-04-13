from .models import Notification

def send_notification(user, title, message, notif_type='general', order_id=''):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notif_type=notif_type,
        order_id=order_id,
    )

def notify_order_placed(order):
    send_notification(
        order.user,
        f"Order Placed! #{order.order_id}",
        f"Your order of ₹{order.total_price} has been placed successfully. We'll start preparing it soon!",
        notif_type='order_placed',
        order_id=order.order_id,
    )

def notify_order_status(order):
    messages = {
        'preparing': ("👨‍🍳 Kitchen is cooking!", f"Your order #{order.order_id} is being prepared. Estimated time: 20-30 min."),
        'out_for_delivery': ("🛵 Out for Delivery!", f"Your order #{order.order_id} is on the way. Get ready!"),
        'delivered': ("✅ Order Delivered!", f"Your order #{order.order_id} has been delivered. Enjoy your meal! 🍽️"),
        'cancelled': ("❌ Order Cancelled", f"Your order #{order.order_id} has been cancelled. Refund will be processed within 5-7 days."),
    }
    if order.status in messages:
        title, msg = messages[order.status]
        notif_type = f"order_{order.status}" if order.status != 'out_for_delivery' else 'order_out'
        send_notification(order.user, title, msg, notif_type=notif_type, order_id=order.order_id)
