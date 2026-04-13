from .models import UserGameProfile, Badge, PointTransaction
from django.utils import timezone

def get_or_create_game_profile(user):
    profile, _ = UserGameProfile.objects.get_or_create(user=user)
    return profile

def award_points(user, points, reason):
    profile = get_or_create_game_profile(user)
    profile.total_points += points
    # Level up check
    if profile.total_points >= 1000 and profile.level < 4:
        profile.level = 4
    elif profile.total_points >= 500 and profile.level < 3:
        profile.level = 3
    elif profile.total_points >= 200 and profile.level < 2:
        profile.level = 2
    profile.save()
    PointTransaction.objects.create(user=user, points=points, reason=reason)

def update_streak(user):
    profile = get_or_create_game_profile(user)
    today = timezone.now().date()
    if profile.last_order_date:
        diff = (today - profile.last_order_date).days
        if diff == 1:
            profile.current_streak += 1
        elif diff > 1:
            profile.current_streak = 1
    else:
        profile.current_streak = 1
    profile.last_order_date = today
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
    profile.save()
    return profile.current_streak

def check_and_award_badges(user, order):
    profile = get_or_create_game_profile(user)
    awarded = []

    badge_checks = [
        ('first_order',  profile.total_orders == 1,          'First Order',   '🎉', 100),
        ('loyal_5',      profile.total_orders >= 5,           '5 Orders Done', '⭐', 150),
        ('loyal_25',     profile.total_orders >= 25,          '25 Orders!',    '🌟', 300),
        ('big_spender',  float(profile.total_spent) >= 5000,  'Spent ₹5000+',  '💎', 200),
        ('streak_7',     profile.current_streak >= 7,         '7-Day Streak',  '🔥', 250),
        ('streak_30',    profile.current_streak >= 30,        '30-Day Streak', '🏆', 500),
    ]

    for slug, condition, reason, icon, pts in badge_checks:
        if condition:
            badge, _ = Badge.objects.get_or_create(
                slug=slug,
                defaults={'name': reason, 'icon': icon, 'points_reward': pts,
                          'description': f'Earned for: {reason}'}
            )
            if badge not in profile.badges.all():
                profile.badges.add(badge)
                award_points(user, pts, f'Badge earned: {reason}')
                awarded.append(badge)

    return awarded

def on_order_placed(order):
    user = order.user
    profile = get_or_create_game_profile(user)
    profile.total_orders += 1
    profile.total_spent += order.total_price
    profile.save()
    streak = update_streak(user)
    award_points(user, 10, f'Order placed #{order.order_id}')
    badges = check_and_award_badges(user, order)
    return {'streak': streak, 'badges': badges}
