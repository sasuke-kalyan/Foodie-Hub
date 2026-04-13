"""
FoodieHub Seed Script
Run: python manage.py shell < seed_data.py
OR: python seed_data.py (from project root after setting DJANGO_SETTINGS_MODULE)
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodiehub.settings')
django.setup()

from restaurants.models import Restaurant, Category
from menu.models import MenuItem
from coupons.models import Coupon
from accounts.models import User
from owner_dashboard.models import OwnerProfile
from django.utils.text import slugify
from datetime import date, timedelta

print("🌱 Seeding FoodieHub database...")

# ─── Categories ───────────────────────────────────────────────────────────────
cats_data = [
    ('Biryani', 'biryani'), ('Pizza', 'pizza'), ('Cafe', 'cafe'),
    ('Chinese', 'chinese'), ('Desserts', 'desserts'), ('Burgers', 'burgers'),
    ('Andhra', 'andhra'), ('Vegetarian', 'vegetarian'),
    ('Street Food', 'street-food'), ('South Indian', 'south-indian'),
]
categories = {}
for name, slug in cats_data:
    cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
    categories[name] = cat
print(f"  ✅ {len(categories)} categories created")

# ─── Restaurants ──────────────────────────────────────────────────────────────
restaurants_data = [
    {
        'name': 'Biryani House', 'cuisine_type': 'Mughlai, Biryani',
        'description': 'Authentic Hyderabadi dum biryani made with fragrant basmati rice, tender meat, and aromatic spices. A culinary legacy since 1980.',
        'delivery_time': '35-45 min', 'delivery_charge': 40, 'min_order': 199,
        'is_veg': False, 'offer_text': '20% OFF on first order', 'city': 'Hyderabad',
        'category': 'Biryani', 'address': '12 MG Road, Secunderabad','image':'foodiehub_complete\media\restaurants\biryani.jpg'
    },
    {
        'name': 'Pizza Corner', 'cuisine_type': 'Italian, Pizza, Pasta',
        'description': 'Hand-tossed wood-fired pizzas with premium toppings, fresh ingredients, and secret Italian sauce. Every bite tells a story.',
        'delivery_time': '25-35 min', 'delivery_charge': 35, 'min_order': 149,
        'is_veg': False, 'offer_text': 'Buy 1 Get 1 Free', 'city': 'Hyderabad',
        'category': 'Pizza', 'address': '45 Banjara Hills Road No. 12',
    },
    {
        'name': 'Cafe Chill', 'cuisine_type': 'Cafe, Continental, Beverages',
        'description': 'Your neighbourhood cafe serving artisan coffee, freshly baked pastries, and light bites. Perfect for any time of day.',
        'delivery_time': '20-30 min', 'delivery_charge': 30, 'min_order': 99,
        'is_veg': True, 'offer_text': 'Free coffee with ₹299+', 'city': 'Hyderabad',
        'category': 'Cafe', 'address': '7 Jubilee Hills Checkpost',
    },
    {
        'name': 'Chinese Express', 'cuisine_type': 'Chinese, Asian, Indo-Chinese',
        'description': 'Fast and delicious Indo-Chinese flavours. From wok-tossed noodles to crispy Manchurian, we bring China to your doorstep.',
        'delivery_time': '30-40 min', 'delivery_charge': 40, 'min_order': 149,
        'is_veg': False, 'offer_text': '15% off on ₹400+', 'city': 'Hyderabad',
        'category': 'Chinese', 'address': '23 Ameerpet Main Road',
    },
    {
        'name': 'Dessert Hub', 'cuisine_type': 'Desserts, Ice Cream, Sweets',
        'description': 'Indulge in handcrafted desserts, premium ice creams, and traditional sweets made with love. Life is sweet here.',
        'delivery_time': '20-30 min', 'delivery_charge': 25, 'min_order': 99,
        'is_veg': True, 'offer_text': 'Free dessert on ₹499+', 'city': 'Hyderabad',
        'category': 'Desserts', 'address': '88 Kukatpally Housing Board',
    },
    {
        'name': 'Burger Town', 'cuisine_type': 'American, Burgers, Fast Food',
        'description': 'Juicy smash burgers, crispy fries, and shakes that hit different. Loaded with real ingredients, no compromises.',
        'delivery_time': '20-30 min', 'delivery_charge': 30, 'min_order': 129,
        'is_veg': False, 'offer_text': 'Combo meals from ₹199', 'city': 'Hyderabad',
        'category': 'Burgers', 'address': '56 Madhapur Hi-Tech City',
    },
    {
        'name': 'Andhra Spice', 'cuisine_type': 'Andhra, Telugu, Spicy',
        'description': 'Fiery Andhra cuisine with traditional gongura curries, spicy chicken fry, and authentic pesarattu. Real Andhra taste guaranteed.',
        'delivery_time': '35-45 min', 'delivery_charge': 40, 'min_order': 149,
        'is_veg': False, 'offer_text': 'Thali at ₹149', 'city': 'Hyderabad',
        'category': 'Andhra', 'address': '34 Dilsukhnagar Main Road',
    },
    {
        'name': 'Veg Delight', 'cuisine_type': 'Pure Vegetarian, North Indian',
        'description': 'A pure vegetarian paradise offering rich dals, creamy paneer dishes, fresh rotis, and wholesome thalis. 100% veg, 100% delicious.',
        'delivery_time': '30-40 min', 'delivery_charge': 35, 'min_order': 149,
        'is_veg': True, 'offer_text': 'Pure Veg | 10% off', 'city': 'Hyderabad',
        'category': 'Vegetarian', 'address': '12 Himayatnagar Cross Roads',
    },
    {
        'name': 'Street Food Adda', 'cuisine_type': 'Street Food, Chaat, Snacks',
        'description': 'All your favourite street food reimagined hygienically. Pani puri, bhel, vada pav, and much more — street taste, home delivery.',
        'delivery_time': '25-35 min', 'delivery_charge': 25, 'min_order': 79,
        'is_veg': True, 'offer_text': '₹29 delivery on first order', 'city': 'Hyderabad',
        'category': 'Street Food', 'address': '9 Begumpet Station Road',
    },
    {
        'name': 'South Indian Tiffins', 'cuisine_type': 'South Indian, Tiffin, Breakfast',
        'description': 'Authentic South Indian breakfast and tiffin — crispy dosas, fluffy idlis, hot sambar and fresh coconut chutney made every morning.',
        'delivery_time': '25-35 min', 'delivery_charge': 30, 'min_order': 99,
        'is_veg': True, 'offer_text': 'Free filter coffee', 'city': 'Hyderabad',
        'category': 'South Indian', 'address': '67 SR Nagar Colony',
    },
]

restaurants = {}
for data in restaurants_data:
    cat_name = data.pop('category')
    slug = slugify(data['name'])
    rest, created = Restaurant.objects.get_or_create(
        slug=slug,
        defaults={**data, 'category': categories.get(cat_name), 'phone': '040-12345678'}
    )
    restaurants[data['name']] = rest
print(f"  ✅ {len(restaurants)} restaurants created")

# ─── Menu Items ───────────────────────────────────────────────────────────────
menu_data = {
    'Biryani House': [
        ('Hyderabadi Chicken Dum Biryani', 'Main Course', 299, False, True, 'Slow-cooked succulent chicken layered with fragrant basmati rice, caramelised onions, fresh mint, and saffron. Sealed with dough and cooked on dum for 45 minutes. Served with raita and mirchi ka salan. A Hyderabadi classic that defines biryani.'),
        ('Mutton Biryani', 'Main Course', 349, False, True, 'Tender slow-cooked mutton pieces marinated in yogurt and spices, layered with long-grain basmati rice and caramelised onions. Finished with kewra water and fried onions. Rich, aromatic and absolutely unforgettable.'),
        ('Veg Biryani', 'Main Course', 199, True, False, 'Fresh seasonal vegetables and paneer slow-cooked with whole spices, then layered with saffron-infused basmati rice. Light yet flavourful, perfect for vegetarians craving the biryani experience.'),
        ('Prawn Biryani', 'Main Course', 379, False, False, 'Plump juicy prawns marinated in coastal spices and cooked with aromatic basmati rice. A seafood lover\'s dream biryani with the perfect balance of heat and flavour.'),
        ('Egg Biryani', 'Main Course', 229, False, False, 'Perfectly boiled eggs coated in spicy masala layered with saffron rice. A budget-friendly biryani that doesn\'t compromise on taste. Great for egg lovers.'),
        ('Chicken 65', 'Starters', 219, False, True, 'Crispy deep-fried chicken pieces marinated in a secret blend of spices, curry leaves and chillies. A classic South Indian starter that\'s perfectly crunchy on the outside and juicy inside.'),
        ('Shammi Kebab', 'Starters', 249, False, False, 'Minced mutton patties mixed with lentils, spices and herbs, pan-fried to golden perfection. Served with mint chutney and onion rings.'),
        ('Mirchi Ka Salan', 'Starters', 99, True, False, 'Traditional Hyderabadi chilli curry with roasted peanuts, sesame and tamarind. The perfect companion to any biryani. Rich, tangy and mildly spicy.'),
        ('Sheer Khurma', 'Desserts', 129, True, False, 'Traditional Hyderabadi dessert made with fine vermicelli cooked in full-cream milk, dry fruits, dates and rose water. Thick, creamy and indulgent.'),
        ('Double Ka Meetha', 'Desserts', 119, True, True, 'Classic Hyderabadi bread pudding made with fried bread, condensed milk, dry fruits and saffron. A royal dessert served at every celebration.'),
        ('Lassi', 'Beverages', 79, True, False, 'Thick creamy yogurt-based drink, available sweet or salted. Made fresh daily with full-fat curd and topped with a dollop of malai.'),
        ('Raita', 'Snacks', 59, True, False, 'Cool and refreshing boondi raita or mixed vegetable raita served alongside biryani. Made with fresh curd, roasted cumin and fresh coriander.'),
        ('Mutton Korma', 'Main Course', 319, False, False, 'Tender mutton slow-cooked in a rich gravy of cashew paste, yogurt, and whole aromatic spices. A Mughlai royal dish served with naan.'),
        ('Chicken Shorba', 'Starters', 149, False, False, 'Traditional Hyderabadi chicken soup slow-cooked with ginger, whole spices and fresh herbs. Light, aromatic and deeply comforting.'),
        ('Dum Ka Murg', 'Main Course', 289, False, True, 'Whole chicken pieces marinated in a blend of yogurt, fried onion paste and aromatic spices, then slow-cooked in their own juices for deep flavour.'),
    ],
    'Pizza Corner': [
        ('Margherita Pizza', 'Main Course', 199, True, True, 'Classic Neapolitan pizza with hand-tossed base, San Marzano tomato sauce, fresh mozzarella and basil. Simple, elegant and absolutely perfect. Our best-selling pizza since day one.'),
        ('Chicken Tikka Pizza', 'Main Course', 299, False, True, 'Fusion of Indian and Italian flavours — tandoori chicken tikka, capsicum, onion and mozzarella on our signature tomato base. A crowd favourite that never disappoints.'),
        ('Veggie Supreme', 'Main Course', 249, True, False, 'Loaded with colourful bell peppers, black olives, mushrooms, sweet corn, onion and cherry tomatoes. Fresh vegetables on a crispy hand-tossed base.'),
        ('BBQ Chicken Pizza', 'Main Course', 319, False, False, 'Smoky BBQ sauce base with grilled chicken strips, caramelised onion, cheddar and mozzarella. Finished with a drizzle of honey for the perfect sweet-savoury balance.'),
        ('Paneer Makhani Pizza', 'Main Course', 279, True, False, 'Creamy makhani sauce topped with soft paneer cubes, capsicum and mozzarella. India\'s favourite flavour on a pizza base — rich, creamy and irresistible.'),
        ('Pasta Arrabbiata', 'Main Course', 229, True, False, 'Penne pasta in a fiery tomato sauce with garlic, olive oil and red chillies. Simple Roman comfort food with a beautiful kick of heat.'),
        ('Garlic Bread', 'Starters', 99, True, True, 'Toasted artisan bread slathered in herb butter and roasted garlic. Baked until golden and served with marinara dipping sauce. Perfect starter.'),
        ('Bruschetta', 'Starters', 129, True, False, 'Grilled bread topped with fresh tomatoes, basil, garlic and extra-virgin olive oil. A simple Italian appetiser bursting with freshness.'),
        ('Cheesy Fries', 'Snacks', 149, True, False, 'Crispy golden fries smothered in warm cheese sauce, topped with jalapeños and fresh herbs. The perfect indulgent snack with every order.'),
        ('Tiramisu', 'Desserts', 179, True, True, 'Classic Italian dessert with espresso-soaked ladyfingers layered with mascarpone cream and dusted with premium cocoa. Authentic Italian recipe, made fresh daily.'),
        ('Choco Lava Cake', 'Desserts', 149, True, False, 'Warm chocolate sponge with a molten chocolate core that flows out on cutting. Served with a scoop of vanilla ice cream. The ultimate chocolate indulgence.'),
        ('Cold Coffee', 'Beverages', 119, True, False, 'Rich espresso blended with chilled milk, sugar and ice cream. Topped with whipped cream and chocolate drizzle. Your perfect coffee pick-me-up.'),
        ('Mocktail Fiesta', 'Beverages', 129, True, False, 'Refreshing blend of tropical fruit juices — mango, passion fruit and orange — with a splash of soda. Vibrant colours, refreshing taste.'),
        ('Focaccia Bread', 'Breads', 139, True, False, 'Italian flatbread baked with olive oil, rosemary, sea salt and cherry tomatoes. Soft inside, crispy outside. Perfect with soup or on its own.'),
        ('Calzone', 'Main Course', 259, False, False, 'Folded pizza stuffed with ricotta, mozzarella, chicken and vegetables. Baked until golden and served with marinara sauce on the side.'),
    ],
    'Cafe Chill': [
        ('Cappuccino', 'Beverages', 129, True, True, 'Perfectly balanced espresso with velvety steamed milk and a thick layer of silky microfoam. Our baristas have perfected this classic Italian coffee over years of practice.'),
        ('Cold Brew Coffee', 'Beverages', 149, True, True, 'Coffee steeped for 18 hours in cold water for a smooth, low-acid, naturally sweet concentrate. Served over ice with a splash of milk. Pure coffee perfection.'),
        ('Avocado Toast', 'Snacks', 199, True, True, 'Sourdough toast topped with smashed avocado, cherry tomatoes, feta cheese, microgreens and a drizzle of olive oil. Instagram-worthy and absolutely delicious.'),
        ('Club Sandwich', 'Snacks', 219, False, False, 'Triple-decker sandwich with grilled chicken, bacon, lettuce, tomato, egg and cheese. Served with a side of fries. The ultimate cafe classic.'),
        ('Croissant', 'Breads', 119, True, True, 'Buttery, flaky French pastry baked fresh every morning. Plain, chocolate or almond filled — each one perfectly laminated with 27 layers of buttery goodness.'),
        ('Blueberry Muffin', 'Desserts', 109, True, False, 'Moist, fluffy muffin packed with plump fresh blueberries and a crunchy sugar crust on top. Baked fresh daily, best enjoyed warm.'),
        ('Pancake Stack', 'Snacks', 229, True, False, 'Fluffy buttermilk pancakes stacked high with maple syrup, fresh berries and whipped cream. Our signature weekend brunch item available all day.'),
        ('French Toast', 'Snacks', 179, True, False, 'Thick brioche soaked in vanilla custard and pan-fried until golden. Served with berry compote, powdered sugar and fresh cream.'),
        ('Waffle', 'Desserts', 199, True, True, 'Belgian waffle made fresh to order — crispy outside, fluffy inside. Topped with Nutella, banana slices, strawberries and whipped cream.'),
        ('Brownie Sundae', 'Desserts', 169, True, True, 'Warm fudgy chocolate brownie topped with a scoop of vanilla ice cream, hot fudge sauce and sprinkles. The best of both worlds.'),
        ('Green Smoothie', 'Beverages', 159, True, False, 'Spinach, banana, mango, coconut water and chia seeds blended into a nutrient-packed smoothie. Energise your morning the healthy way.'),
        ('Matcha Latte', 'Beverages', 169, True, False, 'Ceremonial grade matcha whisked with steamed oat milk and a touch of honey. Earthy, creamy and beautifully vibrant green.'),
        ('Quiche Lorraine', 'Snacks', 189, False, False, 'Classic French tart with a buttery pastry shell filled with cream, egg, bacon and Gruyère cheese. Served with a side salad.'),
        ('Caesar Salad', 'Snacks', 199, True, False, 'Crisp romaine lettuce, house-made Caesar dressing, Parmesan shavings, croutons and a squeeze of lemon. A timeless classic done right.'),
        ('Hot Chocolate', 'Beverages', 139, True, False, 'Rich Belgian chocolate melted into creamy full-fat milk, topped with marshmallows and whipped cream. The ultimate comfort drink for cold evenings.'),
    ],
    'Chinese Express': [
        ('Veg Hakka Noodles', 'Main Course', 169, True, True, 'Thin egg noodles stir-fried with crisp vegetables — cabbage, carrot, capsicum — in a light soy and sesame sauce. Quick, satisfying and full of flavour.'),
        ('Chicken Fried Rice', 'Main Course', 199, False, True, 'Wok-tossed rice with shredded chicken, egg, spring onion and vegetables in our signature soy-garlic sauce. Smoky, fragrant and perfectly balanced.'),
        ('Veg Manchurian', 'Starters', 159, True, True, 'Crispy vegetable dumplings fried golden and tossed in a spicy, tangy Manchurian sauce with garlic, ginger and spring onions. A classic Indo-Chinese starter.'),
        ('Chicken Manchurian', 'Starters', 199, False, True, 'Crispy fried chicken balls in a rich, spicy Manchurian gravy with garlic, ginger, chilli and spring onions. Addictively good.'),
        ('Hot & Sour Soup', 'Starters', 129, True, False, 'Classic Chinese soup with a perfect balance of heat from white pepper and sourness from vinegar. Filled with mushrooms, tofu and vegetables.'),
        ('Dim Sum Basket', 'Starters', 179, True, False, 'Steamed rice flour dumplings filled with seasoned vegetables and served with dipping sauce. Delicate, light and utterly delicious.'),
        ('Schezwan Fried Rice', 'Main Course', 189, True, False, 'Fried rice tossed in our fiery homemade Schezwan sauce with vegetables and crunchy cashews. For those who like it spicy!'),
        ('Kung Pao Chicken', 'Main Course', 229, False, False, 'Diced chicken stir-fried with peanuts, dried chillies and Sichuan peppers in a spicy-sweet sauce. A bold, authentic Chinese classic.'),
        ('Spring Rolls', 'Snacks', 149, True, False, 'Crispy rolls stuffed with stir-fried vegetables and glass noodles, deep-fried until golden. Served with sweet chilli dipping sauce.'),
        ('Chilli Garlic Noodles', 'Main Course', 179, True, False, 'Noodles tossed in a bold chilli-garlic oil with vegetables and a hint of sesame. Simple yet packed with deep, complex flavour.'),
        ('Honey Chilli Potato', 'Snacks', 159, True, True, 'Crispy potato fingers tossed in a sweet, spicy honey-chilli glaze with sesame seeds and spring onions. Impossible to stop eating.'),
        ('Fried Wonton', 'Starters', 169, False, False, 'Minced chicken and prawn filled wontons, deep-fried until crispy. Served with hot chilli sauce and sweet soy for dipping.'),
        ('Fortune Cookies', 'Desserts', 79, True, False, 'Crispy vanilla fortune cookies with surprise messages inside. The perfect sweet ending to a Chinese feast.'),
        ('Lychee Juice', 'Beverages', 99, True, False, 'Fresh lychee blended into a sweet, refreshing drink. Light, tropical and the perfect palate cleanser between courses.'),
        ('Chilli Oil Ramen', 'Main Course', 219, False, False, 'Rich chicken broth with ramen noodles, soft-boiled egg, bamboo shoots and a generous drizzle of homemade chilli oil. Soul-warming comfort food.'),
    ],
    'Dessert Hub': [
        ('Belgian Chocolate Ice Cream', 'Desserts', 129, True, True, 'Rich, creamy ice cream made with 72% Belgian dark chocolate. Dense, decadent and intensely chocolatey. Served in a waffle cone or cup.'),
        ('Mango Sorbet', 'Desserts', 109, True, True, 'Fresh Alphonso mango blended into a smooth, tangy sorbet. Dairy-free, vibrant and the purest expression of Indian summer mangoes.'),
        ('Gulab Jamun', 'Desserts', 89, True, True, 'Soft, pillowy khoya dumplings soaked in rose-scented sugar syrup. Served warm, they melt in your mouth. The classic Indian celebration dessert.'),
        ('Rasgulla', 'Desserts', 79, True, False, 'Spongy chenna balls cooked in light sugar syrup. Soft, delicate and perfectly sweet. A Bengali classic loved across India.'),
        ('Chocolate Fondue', 'Desserts', 249, True, True, 'Rich Belgian chocolate melted to perfection, served with fresh strawberries, banana slices, marshmallows and brownie bites for dipping.'),
        ('Kulfi', 'Desserts', 99, True, True, 'Traditional Indian frozen dessert with a denser texture than ice cream. Available in mango, pista, rose and malai flavours. Each one made from reduced full-fat milk.'),
        ('Cheesecake', 'Desserts', 179, True, True, 'New York-style baked cheesecake on a buttery graham cracker base. Smooth, creamy filling with a gentle vanilla flavour. Available in classic and blueberry.'),
        ('Panna Cotta', 'Desserts', 159, True, False, 'Silky Italian cream dessert set with gelatin and served with a seasonal berry coulis. Delicate, elegant and perfectly wobbles when you touch it.'),
        ('Halwa', 'Desserts', 99, True, False, 'Traditional Indian semolina halwa made with ghee, sugar and dry fruits. Warm, comforting and deeply nostalgic. Exactly like home.'),
        ('Milkshake', 'Beverages', 139, True, True, 'Thick, creamy milkshakes blended with premium ice cream. Available in chocolate, strawberry, vanilla, mango and Oreo. Each one topped with whipped cream.'),
        ('Falooda', 'Beverages', 149, True, True, 'Classic rose-flavoured cold drink with basil seeds, vermicelli, rose syrup, milk and a scoop of kulfi. A complete dessert in a glass.'),
        ('Waffle Cone', 'Desserts', 119, True, False, 'Freshly baked waffle cone with two scoops of your choice of ice cream. Crispy, buttery and the perfect vessel for premium ice cream.'),
        ('Rice Kheer', 'Desserts', 89, True, False, 'Slow-cooked rice pudding with full-fat milk, sugar, cardamom and dry fruits. Garnished with saffron and rose petals. A timeless Indian classic.'),
        ('Brownie', 'Desserts', 129, True, True, 'Dense, fudgy chocolate brownie with a crackly top and gooey centre. Made with 70% dark chocolate, quality butter and minimal flour for maximum chocolate impact.'),
        ('Mango Lassi', 'Beverages', 119, True, True, 'Thick, creamy Alphonso mango blended with full-fat yogurt and a hint of cardamom. Sweet, tangy and utterly refreshing. A classic Indian summer drink.'),
    ],
    'Burger Town': [
        ('Classic Beef Burger', 'Main Course', 229, False, True, 'Double smash patty with American cheese, pickles, onion, mustard and ketchup on a toasted brioche bun. The burger that started it all. No frills, just flavour.'),
        ('Crispy Chicken Burger', 'Main Course', 219, False, True, 'Crispy buttermilk fried chicken thigh with coleslaw, pickles and house sauce on a toasted bun. Crunchy, juicy and absolutely satisfying.'),
        ('Veggie Burger', 'Main Course', 189, True, True, 'House-made black bean and beetroot patty with lettuce, tomato, red onion and avocado aioli. Packed with flavour, 100% plant-based.'),
        ('BBQ Bacon Burger', 'Main Course', 269, False, False, 'Beef patty topped with crispy bacon, cheddar, BBQ sauce, jalapeño and crispy onion strings. Bold flavours stacked high. For serious burger lovers.'),
        ('Mushroom Swiss Burger', 'Main Course', 239, True, False, 'Sautéed mushrooms, Swiss cheese, caramelised onions and truffle aioli on a brioche bun. Earthy, rich and deeply satisfying.'),
        ('Loaded Fries', 'Snacks', 169, True, False, 'Crispy fries smothered in cheese sauce, sour cream, spring onion, bacon bits and pickled jalapeños. A full meal in a box.'),
        ('Onion Rings', 'Snacks', 129, True, True, 'Thick-cut onion rings in a crispy beer batter, fried golden and served with ranch dipping sauce. Crunchy, sweet and impossibly addictive.'),
        ('Chicken Wings', 'Starters', 249, False, True, 'Crispy chicken wings tossed in your choice of sauce — buffalo hot, honey garlic, BBQ or lemon pepper. Served with blue cheese dip.'),
        ('Mozzarella Sticks', 'Starters', 179, True, False, 'Breaded and fried mozzarella sticks with a gooey stretch and crispy exterior. Served with marinara dipping sauce. Impossible to eat just one.'),
        ('Cheeseburger Sliders', 'Snacks', 199, False, False, 'Three mini smash burgers with American cheese, pickles and special sauce on soft slider buns. Perfect for sharing or not — we don\'t judge.'),
        ('Milkshake', 'Beverages', 149, True, True, 'Thick hand-spun milkshakes in chocolate, vanilla, strawberry and seasonal specials. Made with real ice cream and whole milk. Retro vibes, modern taste.'),
        ('Lemonade', 'Beverages', 99, True, False, 'Freshly squeezed lemon juice with mint, sugar and a pinch of black salt. Served over crushed ice. The ultimate thirst quencher.'),
        ('Brownie Ice Cream Sandwich', 'Desserts', 179, True, True, 'Two fudgy brownies sandwiching a generous scoop of vanilla ice cream, rolled in chocolate chips. A childhood dream made adult-sized.'),
        ('Coleslaw', 'Snacks', 89, True, False, 'Creamy house-made coleslaw with shredded cabbage, carrot and a tangy dressing. The perfect burger companion.'),
        ('Chicken Nuggets', 'Snacks', 169, False, False, 'Juicy chicken pieces in a crispy seasoned coating, served with your choice of dipping sauce. The kids love them, and honestly, so do adults.'),
    ],
    'Andhra Spice': [
        ('Gongura Chicken', 'Main Course', 289, False, True, 'Tangy sorrel leaf (gongura) cooked with tender chicken pieces in Andhra-style spices. The unique sourness of gongura paired with fiery heat is the hallmark of Andhra cuisine.'),
        ('Pesarattu', 'Starters', 119, True, True, 'Crispy green moong dal crepes served with ginger chutney and upma stuffing. Traditional Telugu breakfast that\'s healthy, filling and irresistibly delicious.'),
        ('Andhra Chicken Curry', 'Main Course', 269, False, True, 'Bone-in chicken cooked in a fiery red masala with dried red chillies, coconut and whole spices. Authentically spicy Andhra style — not for the faint-hearted!'),
        ('Mutton Pulusu', 'Main Course', 319, False, False, 'Mutton slow-cooked in a tamarind-based gravy with onions, tomatoes and traditional Andhra spices. Tangy, rich and deeply flavourful.'),
        ('Chicken Fry', 'Starters', 249, False, True, 'Andhra-style dry chicken fry with curry leaves, dried red chillies and a bold spice rub. Crispy outside, juicy inside. The iconic Andhra chicken preparation.'),
        ('Pappu (Dal)', 'Main Course', 119, True, True, 'Slow-cooked toor dal tempered with mustard, curry leaves, dry red chilli and ghee. Simple Andhra comfort food that pairs perfectly with rice.'),
        ('Gutti Vankaya', 'Main Course', 179, True, True, 'Baby brinjals stuffed with spiced peanut-sesame masala and slow-cooked in a tangy gravy. A signature Andhra vegetarian delicacy.'),
        ('Royyala Iguru', 'Main Course', 329, False, False, 'Fresh prawns dry-cooked with onion, green chilli, curry leaves and Andhra spices. Fiery, aromatic and absolutely addictive.'),
        ('Uggani', 'Snacks', 89, True, False, 'Puffed rice sautéed with onion, green chilli, mustard and curry leaves. A quick, light Rayalaseema snack that\'s loved across Andhra.'),
        ('Idli Sambar', 'Starters', 99, True, False, 'Soft steamed rice idlis served with piping hot sambar and coconut chutney. Simple, healthy and perfect any time of day.'),
        ('Andhra Meals', 'Main Course', 199, False, True, 'Full Andhra thali with rice, pappu, sambar, rasam, curries, pickles, papad and dessert. A complete meal that celebrates the richness of Telugu cuisine.'),
        ('Rasam', 'Beverages', 69, True, False, 'Thin, tangy tomato and tamarind soup with pepper, cumin and curry leaves. A digestive after-meal drink or a light starter soup.'),
        ('Bobbatlu', 'Desserts', 109, True, True, 'Sweet flatbread stuffed with chana dal and jaggery, cooked on a griddle with ghee. Traditional Telugu festival sweet that\'s soft, rich and utterly satisfying.'),
        ('Payasam', 'Desserts', 119, True, False, 'Creamy rice pudding made with full-fat milk, jaggery, cardamom and dry fruits. Served warm or chilled, it\'s the quintessential South Indian dessert.'),
        ('Gongura Pickle', 'Snacks', 79, True, False, 'Andhra\'s most famous condiment — tangy sorrel leaf pickle tempered with sesame oil, red chillies and mustard. Perfect accompaniment to any meal.'),
    ],
    'Veg Delight': [
        ('Paneer Butter Masala', 'Main Course', 239, True, True, 'Soft cottage cheese cubes in a rich, velvety tomato-cream sauce with aromatic spices. Mild, creamy and utterly indulgent. Best enjoyed with garlic naan.'),
        ('Dal Makhani', 'Main Course', 199, True, True, 'Black lentils slow-cooked overnight with kidney beans, tomatoes, cream and butter. Rich, smoky and deeply flavourful. The crown jewel of North Indian cooking.'),
        ('Palak Paneer', 'Main Course', 219, True, False, 'Fresh spinach purée with soft paneer cubes, tempered with garam masala and cream. Vibrant, nutritious and a classic vegetarian curry loved by all.'),
        ('Chole Bhature', 'Main Course', 169, True, True, 'Spicy, tangy Punjabi chickpea curry served with deep-fried fluffy bhature. The ultimate North Indian comfort meal. Rich gravy, crispy bread — perfection.'),
        ('Mixed Veg Curry', 'Main Course', 189, True, False, 'Seasonal vegetables cooked in a spiced tomato-onion gravy. Simple, wholesome and deeply satisfying everyday Indian cooking at its finest.'),
        ('Aloo Gobi', 'Main Course', 169, True, False, 'Potatoes and cauliflower cooked with turmeric, ginger and dry spices in a traditional North Indian style. Simple, comforting and always delicious.'),
        ('Jeera Rice', 'Main Course', 129, True, True, 'Basmati rice tempered with cumin seeds and ghee. Light, fragrant and the perfect companion to any rich curry.'),
        ('Garlic Naan', 'Breads', 49, True, True, 'Soft leavened flatbread with roasted garlic and butter, baked in a tandoor. Perfectly charred with buttery, garlicky goodness in every bite.'),
        ('Butter Roti', 'Breads', 35, True, True, 'Whole wheat flatbread baked in a tandoor and finished with fresh butter. Light, wholesome and perfect for scooping up curry.'),
        ('Puri', 'Breads', 39, True, False, 'Deep-fried whole wheat flatbreads that puff up beautifully. Light, crispy and perfect with any curry or pickle.'),
        ('Raita', 'Snacks', 69, True, False, 'Fresh yogurt with cucumber, tomato, onion and roasted cumin. A cool and refreshing contrast to spicy curries.'),
        ('Papad', 'Snacks', 49, True, False, 'Crispy roasted or fried lentil wafers. Light, crunchy and the perfect accompaniment to any Indian meal. Masala, plain or roasted available.'),
        ('Gulab Jamun', 'Desserts', 89, True, True, 'Soft khoya milk dumplings soaked in rose and cardamom sugar syrup. The most beloved Indian dessert, served warm. Pure nostalgia in every bite.'),
        ('Lassi', 'Beverages', 89, True, True, 'Thick, creamy yogurt drink available sweet or salted. Made with full-fat dahi and topped with a generous dollop of malai.'),
        ('Paneer Tikka', 'Starters', 229, True, True, 'Cottage cheese cubes marinated in spiced yogurt and chargrilled in a tandoor. Smoky, flavourful and the best Indian vegetarian starter.'),
    ],
    'Street Food Adda': [
        ('Pani Puri', 'Snacks', 79, True, True, 'Crispy hollow puris filled with spiced potato and chickpea mix, dipped in tangy, minty ice-cold flavoured water. The most addictive street food in India. Six puris per serving.'),
        ('Bhel Puri', 'Snacks', 89, True, True, 'Puffed rice tossed with chopped tomatoes, onions, coriander, sev, tamarind chutney and green chutney. Light, tangy, crunchy and absolutely delicious.'),
        ('Sev Puri', 'Snacks', 89, True, True, 'Crispy puris topped with boiled potato, chutneys, onion, tomato and generous amounts of sev. Each bite is a perfect mix of textures and flavours.'),
        ('Dahi Puri', 'Snacks', 99, True, False, 'Crispy puris filled with potato, topped with thick sweet yogurt, tamarind chutney, green chutney and sev. Cool, tangy and utterly refreshing.'),
        ('Vada Pav', 'Snacks', 59, True, True, 'Mumbai\'s legendary street burger — spiced potato vada in a soft pav with dry garlic chutney and green chutney. Simple, filling and incredibly satisfying.'),
        ('Pav Bhaji', 'Main Course', 139, True, True, 'Buttery mixed vegetable mash served with toasted, butter-soaked pav. Mumbai\'s most iconic street food, generously topped with butter, onion and lemon.'),
        ('Masala Corn', 'Snacks', 79, True, False, 'Steamed sweet corn kernels tossed with butter, chaat masala, lemon and fresh coriander. A simple, irresistible evening snack.'),
        ('Aloo Tikki', 'Snacks', 89, True, True, 'Crispy spiced potato patties served with chole, green chutney and tamarind. Pan-fried to a perfect golden crust. Delhi\'s favourite street snack.'),
        ('Samosa', 'Snacks', 49, True, True, 'Crispy fried pastry filled with spiced potato and peas. Served with mint chutney and tamarind sauce. India\'s most beloved snack, perfected here.'),
        ('Kachori', 'Snacks', 59, True, False, 'Flaky deep-fried pastry stuffed with spiced moong dal or peas. Crispy, flavourful and best enjoyed with tamarind chutney.'),
        ('Chaat Platter', 'Snacks', 179, True, True, 'A generous platter with pani puri, bhel, aloo tikki and sev puri. The ultimate chaat experience for two. Four street foods in one box.'),
        ('Dabeli', 'Snacks', 79, True, False, 'Kutchi dabeli — spiced potato filling in a toasted pav with chutneys, pomegranate seeds and sev. A Gujarati street food sensation.'),
        ('Sugarcane Juice', 'Beverages', 59, True, True, 'Fresh sugarcane juice with a twist of ginger and lemon. Natural, refreshing and the best accompaniment to spicy chaat.'),
        ('Masala Chaas', 'Beverages', 59, True, True, 'Thin buttermilk tempered with green chilli, ginger, curry leaves and roasted cumin. Light, digestive and perfect with spicy street food.'),
        ('Kulfi Stick', 'Desserts', 69, True, True, 'Traditional Indian frozen dessert on a stick. Denser and creamier than ice cream, available in malai, pista, mango and rose. The street food dessert.'),
    ],
    'South Indian Tiffins': [
        ('Masala Dosa', 'Main Course', 129, True, True, 'Crispy fermented rice crepe stuffed with spiced potato masala, served with sambar and two chutneys. The king of South Indian breakfast. Made fresh on the tawa.'),
        ('Plain Dosa', 'Main Course', 89, True, True, 'Thin, crispy fermented rice and urad dal crepe served with sambar and coconut chutney. Simple, light and perfect for any time of day.'),
        ('Rava Dosa', 'Main Course', 109, True, False, 'Lacy, crispy semolina dosa with green chilli, pepper and curry leaves. Delicate, quick to make and best enjoyed hot right off the tawa.'),
        ('Idli', 'Starters', 79, True, True, 'Soft, fluffy steamed rice cakes served with sambar and coconut chutney. Healthy, light and the perfect South Indian morning meal. Three idlis per serving.'),
        ('Medu Vada', 'Starters', 89, True, True, 'Crispy urad dal fritters in a ring shape, served with sambar and chutney. Crunchy outside, soft inside with a satisfying chew. A South Indian essential.'),
        ('Uttapam', 'Main Course', 119, True, False, 'Thick rice pancake topped with onion, tomato, green chilli and coriander. Soft, filling and more substantial than a dosa. Perfect comfort tiffin.'),
        ('Upma', 'Snacks', 89, True, False, 'Semolina cooked with onion, green chilli, ginger, curry leaves and vegetables. Quick, light and deeply comforting. A traditional South Indian breakfast.'),
        ('Pongal', 'Main Course', 99, True, True, 'Rice and moong dal cooked together with black pepper, ginger, ghee and cashews. The most comforting South Indian dish. Perfect on rainy days.'),
        ('Sambar', 'Starters', 59, True, True, 'Spiced tamarind lentil soup with drumstick, brinjal and pearl onions. Made fresh daily with our 25-spice sambar powder recipe.'),
        ('Coconut Chutney', 'Snacks', 39, True, True, 'Fresh coconut, green chilli, ginger and tempered with mustard seeds and curry leaves. Made fresh throughout the day. The perfect dosa companion.'),
        ('Filter Coffee', 'Beverages', 49, True, True, 'Strong South Indian decoction mixed with hot full-fat milk. Served in a traditional tumbler and davara. The non-negotiable morning ritual.'),
        ('Kesari Bath', 'Desserts', 79, True, True, 'Semolina pudding cooked with ghee, saffron, sugar and garnished with cashews and raisins. Sweet, fragrant and the classic South Indian dessert.'),
        ('Curd Rice', 'Main Course', 99, True, False, 'Soft-cooked rice mixed with fresh curd and tempered with mustard, dried red chilli, ginger and curry leaves. The most comforting end to a South Indian meal.'),
        ('Lemon Rice', 'Main Course', 109, True, False, 'Cooked rice tossed with lemon juice, turmeric, mustard seeds, peanuts and curry leaves. Tangy, fragrant and a South Indian classic loved across the country.'),
        ('Bisi Bele Bath', 'Main Course', 139, True, True, 'Karnataka\'s beloved one-pot dish of rice, lentils and vegetables cooked together with a special spice powder and ghee. Warming, wholesome and utterly satisfying.'),
    ],
}

item_count = 0
for rest_name, items in menu_data.items():
    restaurant = restaurants.get(rest_name)
    if not restaurant:
        continue
    for item_data in items:
        name, cat, price, is_veg, is_bestseller, desc = item_data
        MenuItem.objects.get_or_create(
            restaurant=restaurant,
            name=name,
            defaults={
                'category': cat, 'price': price, 'is_veg': is_veg,
                'is_bestseller': is_bestseller, 'description': desc,
                'is_available': True,
            }
        )
        item_count += 1

print(f"  ✅ {item_count} menu items created")

# ─── Coupons ──────────────────────────────────────────────────────────────────
coupons = [
    {'code': 'SAVE20', 'description': '20% off on orders above ₹300', 'discount_type': 'percent', 'discount_value': 20, 'max_discount': 100, 'min_order_value': 300, 'expiry_date': date.today() + timedelta(days=90), 'usage_limit': 1000},
    {'code': 'FIRST50', 'description': 'Flat ₹50 off on your first order', 'discount_type': 'flat', 'discount_value': 50, 'max_discount': None, 'min_order_value': 199, 'expiry_date': date.today() + timedelta(days=60), 'usage_limit': 500},
    {'code': 'WELCOME10', 'description': '10% off — welcome to FoodieHub!', 'discount_type': 'percent', 'discount_value': 10, 'max_discount': 75, 'min_order_value': 149, 'expiry_date': date.today() + timedelta(days=120), 'usage_limit': 2000},
    {'code': 'BIRYANI30', 'description': '₹30 off on biryani orders', 'discount_type': 'flat', 'discount_value': 30, 'max_discount': None, 'min_order_value': 249, 'expiry_date': date.today() + timedelta(days=45), 'usage_limit': 300},
    {'code': 'WEEKEND25', 'description': '25% off on weekends', 'discount_type': 'percent', 'discount_value': 25, 'max_discount': 150, 'min_order_value': 399, 'expiry_date': date.today() + timedelta(days=30), 'usage_limit': 500},
]

for coupon_data in coupons:
    Coupon.objects.get_or_create(code=coupon_data['code'], defaults=coupon_data)
print(f"  ✅ {len(coupons)} coupons created")

print("\n🎉 Database seeded successfully!")
print("─" * 40)
print("📋 Summary:")
print(f"   • {Restaurant.objects.count()} restaurants")
print(f"   • {MenuItem.objects.count()} menu items")
print(f"   • {Category.objects.count()} categories")
print(f"   • {Coupon.objects.count()} coupons")
print("\n🚀 Next steps:")
print("   1. python manage.py migrate")
print("   2. python manage.py createsuperuser")
print("   3. python manage.py shell < seed_data.py")
print("   4. python manage.py runserver")
