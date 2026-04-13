from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Wishlist
from menu.models import MenuItem

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user).select_related('menu_item__restaurant')
    return render(request, 'wishlist/wishlist.html', {'items': items})

@login_required
def toggle_wishlist(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, menu_item=menu_item)
    if not created:
        obj.delete()
        msg = "Removed from wishlist"
        status = 'removed'
    else:
        msg = "Added to wishlist!"
        status = 'added'
    messages.success(request, msg)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': status})
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:view'))
