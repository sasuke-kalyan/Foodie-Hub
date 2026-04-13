from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from restaurants.models import Restaurant

@login_required
def add_review(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        if Review.objects.filter(user=request.user, restaurant=restaurant).exists():
            messages.warning(request, "You have already reviewed this restaurant.")
        elif not comment:
            messages.error(request, "Please write a comment.")
        else:
            Review.objects.create(user=request.user, restaurant=restaurant, rating=rating, comment=comment)
            messages.success(request, "Review submitted!")
    return redirect('restaurants:detail', slug=restaurant_slug)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    slug = review.restaurant.slug
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect('restaurants:detail', slug=slug)
