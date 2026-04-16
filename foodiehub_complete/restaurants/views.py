from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse   # ✅ NEW LINE ADDED
from .models import Restaurant, Category
from menu.models import MenuItem


def home(request):
    restaurants = Restaurant.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()
    featured = restaurants[:6]
    context = {
        'restaurants': restaurants,
        'categories': categories,
        'featured': featured,
    }
    return render(request, 'restaurants/home.html', context)


def restaurant_list(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    veg_only = request.GET.get('veg', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    rating_filter = request.GET.get('rating', '')

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(cuisine_type__icontains=query) |
            Q(description__icontains=query)
        )
    if category:
        restaurants = restaurants.filter(category__slug=category)
    if veg_only:
        restaurants = restaurants.filter(is_veg=True)

    if rating_filter:
        try:
            min_rating = float(rating_filter)
            filtered = [r for r in restaurants if r.average_rating() >= min_rating]
            restaurants = Restaurant.objects.filter(id__in=[r.id for r in filtered])
        except ValueError:
            pass

    context = {
        'restaurants': restaurants,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'veg_only': veg_only,
        'rating_filter': rating_filter,
    }
    return render(request, 'restaurants/list.html', context)


def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)

    categories_with_items = {}
    for item in menu_items:
        cat = item.category
        if cat not in categories_with_items:
            categories_with_items[cat] = []
        categories_with_items[cat].append(item)

    from reviews.models import Review
    reviews = Review.objects.filter(restaurant=restaurant).order_by('-created_at')
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(restaurant=restaurant, user=request.user).first()

    context = {
        'restaurant': restaurant,
        'categories_with_items': categories_with_items,
        'reviews': reviews,
        'user_review': user_review,
        'avg_rating': restaurant.average_rating(),
        'review_count': restaurant.review_count(),
    }
    return render(request, 'restaurants/detail.html', context)


def search_view(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.none()
    menu_items = MenuItem.objects.none()

    if query:
        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(cuisine_type__icontains=query), is_active=True
        )
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query), is_available=True
        )

    context = {
        'query': query,
        'restaurants': restaurants,
        'menu_items': menu_items,
    }
    return render(request, 'restaurants/search.html', context)

def live_search(request):
    query = request.GET.get('q', '')
    
    results = []
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)

        for r in restaurants:
            results.append({
                'name': r.name,
                'slug': r.slug,
            })

    return JsonResponse({'results': results})