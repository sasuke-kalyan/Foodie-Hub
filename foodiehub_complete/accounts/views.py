from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileEditForm, DeliveryAddressForm
from .models import DeliveryAddress


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = form.cleaned_data['role']
        user.phone = form.cleaned_data['phone']
        user.save()
        login(request, user)
        messages.success(request, f"Welcome to FoodieHub, {user.username}!")
        if user.role == 'owner':
            return redirect('owner_dashboard:dashboard')
        return redirect('home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Try username or email
        from .models import User
        user = None
        try:
            u = User.objects.get(email=username)
            user = authenticate(request, username=u.username, password=password)
        except User.DoesNotExist:
            user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.role == 'owner':
                return redirect('owner_dashboard:dashboard')
            if user.is_staff:
                return redirect('/admin/')
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password.")
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    addresses = DeliveryAddress.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'addresses': addresses})


@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('accounts:profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def add_address(request):
    form = DeliveryAddressForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        if address.is_default:
            DeliveryAddress.objects.filter(user=request.user).update(is_default=False)
        address.save()
        messages.success(request, "Address added!")
        return redirect('accounts:profile')
    return render(request, 'accounts/add_address.html', {'form': form})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(DeliveryAddress, pk=pk, user=request.user)
    address.delete()
    messages.success(request, "Address deleted.")
    return redirect('accounts:profile')

def set_language(request):
    from django.shortcuts import redirect
    lang = request.POST.get('lang', 'en')
    if lang in ['en', 'te', 'hi']:
        request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))
