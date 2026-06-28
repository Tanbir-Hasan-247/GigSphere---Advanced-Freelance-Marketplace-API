import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# জ্যাঙ্গো এনভায়রনমেন্ট সেটআপ
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreelanceHub.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import SellerProfile, BuyerProfile # তোমার অ্যাপের নাম accounts ধরে নিলাম
from services.models import Category, Service
from orders.models import Order, OrderStatusLog, Notification
from reviews.models import Review
from faker import Faker

fake = Faker()
User = get_user_model()

def populate():
    print("🧹 Cleaning old generated dummy data (optional)...")
    # চাইলে আনকমেন্ট করে পুরনো ডেটা ক্লিয়ার করতে পারো
    # Review.objects.all().delete()
    # Order.objects.all().delete()
    # Service.objects.all().delete()
    # Category.objects.all().delete()
    # User.objects.exclude(is_superuser=True).delete()

    print("🚀 Starting Database Population...")

    # ১. Categories তৈরি করা
    category_names = [
        "Web Development", "Graphic Design", "Digital Marketing", 
        "SEO Optimization", "Content Writing", "Video Editing",
        "Mobile App Development", "Data Entry"
    ]
    categories = []
    for name in category_names:
        cat, created = Category.objects.get_or_create(name=name)
        categories.append(cat)
    print(f"✅ Created {len(categories)} Categories")

    # ২. Users (Sellers & Buyers) তৈরি করা
    sellers = []
    buyers = []

    print("⏳ Creating 15 Sellers & 15 Buyers...")
    for _ in range(15):
        # Seller
        seller_email = fake.unique.email()
        seller = User.objects.create_user(
            email=seller_email, 
            password="password123", 
            phone=fake.phone_number()[:15], 
            role="Seller"
        )
        SellerProfile.objects.create(
            user=seller,
            bio=fake.text(max_nb_chars=200),
            skills="Django, React, Python, Design"
        )
        sellers.append(seller)

        # Buyer
        buyer_email = fake.unique.email()
        buyer = User.objects.create_user(
            email=buyer_email, 
            password="password123", 
            phone=fake.phone_number()[:15], 
            role="Buyer"
        )
        BuyerProfile.objects.create(
            user=buyer,
            bio=fake.text(max_nb_chars=150)
        )
        buyers.append(buyer)
    print(f"✅ Created {len(sellers)} Sellers and {len(buyers)} Buyers")

    # ৩. Services তৈরি করা (Minimum 40)
    print("⏳ Creating 45 Services...")
    services = []
    for _ in range(45):
        seller = random.choice(sellers)
        category = random.choice(categories)
        service = Service.objects.create(
            seller=seller,
            category=category,
            title=fake.sentence(nb_words=6)[:-1], # Remove trailing dot
            description=fake.paragraph(nb_sentences=5),
            price=Decimal(random.randrange(10, 500)),
            delivery_days=random.randint(1, 30),
            requirements=fake.paragraph(nb_sentences=2),
            is_active=True
        )
        services.append(service)
    print(f"✅ Created {len(services)} Services")

    # ৪. Orders তৈরি করা (Minimum 50)
    print("⏳ Creating 50 Orders with different statuses...")
    orders = []
    statuses = ['Pending', 'In Progress', 'Completed', 'Cancelled']
    
    for _ in range(50):
        buyer = random.choice(buyers)
        service = random.choice(services)
        status = random.choice(statuses)
        
        order = Order.objects.create(
            buyer=buyer,
            seller=service.seller,
            service=service,
            status=status,
            price_at_order=service.price,
            requirements_note=fake.paragraph(nb_sentences=2)
        )
        
        # যদি Completed হয় তবে completed_at সেট করা
        if status == 'Completed':
            order.completed_at = timezone.now() - timedelta(days=random.randint(1, 10))
            order.save()

        # OrderStatusLog তৈরি
        OrderStatusLog.objects.create(
            order=order,
            old_status='Pending',
            new_status=status,
            changed_by=service.seller if status in ['In Progress', 'Completed'] else buyer
        )

        # Notification তৈরি
        Notification.objects.create(
            recipient=service.seller,
            order=order,
            message=f"New order placed by {buyer.email} for {service.title}"
        )
        
        orders.append(order)
    print(f"✅ Created {len(orders)} Orders")

    # ৫. Reviews তৈরি করা (শুধু Completed Order এর জন্য)
    print("⏳ Creating Reviews for Completed Orders...")
    completed_orders = [order for order in orders if order.status == 'Completed']
    reviews_count = 0
    
    for order in completed_orders:
        # OneToOne Constraint এর জন্য চেক করে নিচ্ছি
        if not hasattr(order, 'review'):
            Review.objects.create(
                order=order,
                buyer=order.buyer,
                seller=order.seller,
                service=order.service,
                rating=random.randint(3, 5), # সাধারণত ৩-৫ রেটিং বেশি পড়ে
                comment=fake.paragraph(nb_sentences=3)
            )
            reviews_count += 1

    print(f"✅ Created {reviews_count} Reviews")
    print("🎉 Database successfully populated with realistic dummy data!")

if __name__ == '__main__':
    populate()