from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import ChatRoom, ChatMessage
from restaurants.models import Restaurant

@login_required
def chat_room(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    if request.user.role != 'customer':
        messages.error(request, "Only customers can chat with restaurants.")
        return redirect('home')

    room, created = ChatRoom.objects.get_or_create(
        customer=request.user,
        restaurant=restaurant,
    )
    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        if msg_text:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                sender_type='customer',
                message=msg_text,
            )
        return redirect('chat:room', restaurant_slug=restaurant_slug)

    chat_messages = room.messages.all()
    # Mark owner messages as read
    room.messages.filter(sender_type='owner', is_read=False).update(is_read=True)
    return render(request, 'chat/room.html', {
        'room': room,
        'restaurant': restaurant,
        'chat_messages': chat_messages,
    })

@login_required
def owner_chat_list(request):
    if request.user.role != 'owner':
        return redirect('home')
    try:
        restaurant = request.user.owner_profile.restaurant
    except:
        return redirect('owner_dashboard:dashboard')
    rooms = ChatRoom.objects.filter(restaurant=restaurant, is_active=True)
    return render(request, 'chat/owner_list.html', {'rooms': rooms, 'restaurant': restaurant})

@login_required
def owner_chat_room(request, room_id):
    if request.user.role != 'owner':
        return redirect('home')
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        if msg_text:
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                sender_type='owner',
                message=msg_text,
            )
        return redirect('chat:owner_room', room_id=room_id)
    room.messages.filter(sender_type='customer', is_read=False).update(is_read=True)
    return render(request, 'chat/owner_room.html', {'room': room})

@login_required
def get_messages_api(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    after_id = int(request.GET.get('after', 0))
    msgs = room.messages.filter(id__gt=after_id)
    data = [{
        'id': m.id,
        'sender': m.sender.username,
        'sender_type': m.sender_type,
        'message': m.message,
        'time': m.created_at.strftime('%I:%M %p'),
    } for m in msgs]
    return JsonResponse({'messages': data})
