from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile
from accounts.models import User

def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile

@login_required
def my_profile_extra(request):
    profile = get_or_create_profile(request.user)
    referrals = User.objects.filter(profile__referred_by=request.user)
    return render(request, 'profiles/extra.html', {
        'profile': profile,
        'referrals': referrals,
        'referral_link': request.build_absolute_uri(f'/accounts/register/?ref={profile.referral_code}'),
    })

@login_required
def subscribe(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        plan = request.POST.get('plan')
        from datetime import timedelta
        if plan in ['basic', 'premium']:
            profile.subscription_plan = plan
            profile.subscription_expiry = timezone.now().date() + timedelta(days=30)
            profile.save()
            messages.success(request, f"🎉 Subscribed to {plan.title()} plan!")
        return redirect('profiles:extra')
    return render(request, 'profiles/subscribe.html', {'profile': profile})

@login_required
def update_birthday(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        dob = request.POST.get('date_of_birth')
        if dob:
            profile.date_of_birth = dob
            profile.save()
            messages.success(request, "🎂 Birthday saved! You'll get a special offer on your birthday!")
    return redirect('profiles:extra')

def register_with_referral(request):
    ref_code = request.GET.get('ref', '')
    request.session['referral_code'] = ref_code
    return redirect('accounts:register')
