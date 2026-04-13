from django.db import models
from accounts.models import User

class Badge(models.Model):
    BADGE_CHOICES = [
        ('first_order',   'First Order',    ),
        ('loyal_5',       'Loyal Customer', ),
        ('loyal_25',      'Super Fan',      ),
        ('reviewer',      'Food Critic',    ),
        ('big_spender',   'Big Spender',    ),
        ('streak_7',      'Week Warrior',   ),
        ('streak_30',     'Month Master',   ),
        ('referrer',      'Friend Magnet',  ),
        ('night_owl',     'Night Owl',      ),
        ('early_bird',    'Early Bird',     ),
    ]
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, default='🏆')
    color = models.CharField(max_length=7, default='#ffc107')
    points_reward = models.IntegerField(default=50)

    def __str__(self):
        return self.name


class UserGameProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='game_profile')
    total_points = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_order_date = models.DateField(null=True, blank=True)
    level = models.IntegerField(default=1)
    badges = models.ManyToManyField(Badge, blank=True)
    total_orders = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} — Level {self.level} — {self.total_points} pts"

    def get_level_name(self):
        levels = {1: '🥉 Foodie', 2: '🥈 Gourmet', 3: '🥇 Connoisseur', 4: '💎 Legend'}
        return levels.get(self.level, '💎 Legend')

    def points_to_next_level(self):
        thresholds = {1: 200, 2: 500, 3: 1000, 4: 9999}
        return thresholds.get(self.level, 9999) - self.total_points

    def level_progress_percent(self):
        thresholds = {1: 200, 2: 500, 3: 1000, 4: 9999}
        prev = {1: 0, 2: 200, 3: 500, 4: 1000}
        start = prev.get(self.level, 0)
        end = thresholds.get(self.level, 9999)
        if end == start: return 100
        return min(100, int((self.total_points - start) / (end - start) * 100))


class PointTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_transactions')
    points = models.IntegerField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {'+' if self.points > 0 else ''}{self.points} — {self.reason}"
