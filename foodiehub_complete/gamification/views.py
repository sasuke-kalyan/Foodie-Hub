from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserGameProfile, Badge, PointTransaction
from .utils import get_or_create_game_profile

@login_required
def leaderboard(request):
    profiles = UserGameProfile.objects.select_related('user').order_by('-total_points')[:20]
    my_profile = get_or_create_game_profile(request.user)
    recent_transactions = PointTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    all_badges = Badge.objects.all()
    return render(request, 'gamification/leaderboard.html', {
        'profiles': profiles,
        'my_profile': my_profile,
        'recent_transactions': recent_transactions,
        'all_badges': all_badges,
    })

@login_required
def my_rewards(request):
    profile = get_or_create_game_profile(request.user)
    transactions = PointTransaction.objects.filter(user=request.user).order_by('-created_at')[:20]
    all_badges = Badge.objects.all()
    earned_badges = profile.badges.all()
    return render(request, 'gamification/my_rewards.html', {
        'profile': profile,
        'transactions': transactions,
        'all_badges': all_badges,
        'earned_badges': earned_badges,
    })
