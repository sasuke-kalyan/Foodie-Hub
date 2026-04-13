# 🍔 FoodieHub — Complete Production Project

## 🚀 Run in 5 Steps

```bash
pip install django pillow razorpay
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < seed_data.py
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## ✅ All 39+ Features Included

### Core
- 10 restaurants + 300 menu items (auto-seeded)
- Customer register/login/profile
- Restaurant browsing, search, filters
- Cart with coupon system
- Order placement, tracking, history
- Wishlist, Reviews & Ratings
- Owner dashboard, Admin panel

### Batch 1
- 💳 Razorpay payment gateway
- 📊 Revenue charts (owner dashboard)
- 📥 Export orders to CSV
- 🌙 Dark mode toggle
- 📱 PWA (install as mobile app)

### Batch 2
- 🔔 Order notifications (bell icon, auto-poll)
- ⚡ Flash sale with live countdown timer
- 🖨️ Print order receipt

### Batch 3
- 💬 Live chat (customer ↔ restaurant)
- 🎂 Birthday special offers
- 👑 Subscription plans (Basic ₹99 / Premium ₹199)
- 👫 Refer a friend + credits system
- 📧 Email notifications

### Missing Features (now included)
- ⏰ Auto-close restaurant at set time
- 🗺️ City-wise restaurant map view
- 📊 Admin analytics with real charts

### Batch 5
- 🗣️ Voice search (speak to search)
- 🌍 Multi-language (Telugu/Hindi/English)
- ♿ Accessibility toolbar (large text, high contrast, dyslexia font)
- 🎮 Gamification (points, levels, badges, streaks)
- 📸 Food photo gallery (masonry + lightbox)
- 🔍 Advanced filters (price slider, time slider, sort)

---

## 🔑 Add Your API Keys (settings.py)

```python
RAZORPAY_KEY_ID = 'rzp_test_XXXXX'      # razorpay.com
RAZORPAY_KEY_SECRET = 'XXXXX'
GOOGLE_MAPS_API_KEY = 'XXXXX'           # console.cloud.google.com
EMAIL_HOST_USER = 'your@gmail.com'
EMAIL_HOST_PASSWORD = 'app_password'
```

---

## 🔗 All URLs

| Page | URL |
|------|-----|
| Home | / |
| Restaurants | /restaurants/ |
| Flash Sales | /flash-sales/ |
| Offers | /coupons/ |
| Cart | /cart/ |
| Orders | /orders/history/ |
| Wishlist | /wishlist/ |
| Notifications | /notifications/ |
| Live Chat | /chat/r/<restaurant-slug>/ |
| Profile | /accounts/profile/ |
| Rewards | /rewards/rewards/ |
| Subscription | /profile/ |
| Gallery | /gallery/r/<restaurant-slug>/ |
| Owner Dashboard | /owner/ |
| Owner Chat | /chat/owner/ |
| Analytics | /analytics/ |
| City Map | /analytics/map/ |
| Admin | /admin/ |

---

## 🎫 Test Coupons
SAVE20 · FIRST50 · WELCOME10 · BIRYANI30 · WEEKEND25

## 💳 Test Razorpay Card
4111 1111 1111 1111 | Any future date | Any CVV | OTP: 1234
