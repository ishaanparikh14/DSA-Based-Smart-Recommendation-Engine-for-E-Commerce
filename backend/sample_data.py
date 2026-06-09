"""
Sample Data for DSA E-Commerce Engine
Generates realistic product catalog, users, and transaction history
"""

from models import Product, User, Transaction
from datetime import datetime, timedelta
from typing import List
import random


def get_sample_products() -> List[Product]:
    """Generate 89 products across 10 categories with realistic data"""
    products = []
    
    # Electronics (10 products)
    electronics = [
        Product(1, "iPhone 15 Pro", "Electronics", 999.99, 45, "", "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400&h=400&fit=crop"),
        Product(2, "MacBook Pro 16\"", "Electronics", 2499.99, 20, "", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop"),
        Product(3, "iPad Air", "Electronics", 599.99, 35, "", "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"),
        Product(4, "Apple Watch Series 9", "Electronics", 399.99, 50, "", "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=400&fit=crop"),
        Product(5, "AirPods Pro", "Electronics", 249.99, 100, "", "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400&h=400&fit=crop"),
        Product(6, "Samsung Galaxy S24", "Electronics", 899.99, 40, "", "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop"),
        Product(7, "Sony WH-1000XM5", "Electronics", 399.99, 30, "", "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=400&fit=crop"),
        Product(8, "Dell XPS 15", "Electronics", 1799.99, 15, "", "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=400&fit=crop"),
        Product(9, "LG OLED TV 55\"", "Electronics", 1499.99, 12, "", "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400&h=400&fit=crop"),
        Product(10, "Canon EOS R6", "Electronics", 2499.99, 8, "", "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop"),
    ]
    products.extend(electronics)
    
    # Home & Kitchen (8 products)
    home_kitchen = [
        ("Instant Pot Duo", 89.99, 75, "7-in-1 programmable pressure cooker"),
        ("Ninja Air Fryer", 129.99, 60, "Healthy cooking with air frying technology"),
        ("KitchenAid Stand Mixer", 379.99, 25, "Professional-grade stand mixer"),
        ("Dyson V15 Vacuum", 649.99, 20, "Powerful cordless vacuum cleaner"),
        ("Keurig K-Elite", 169.99, 50, "Single-serve coffee maker"),
        ("Vitamix Blender", 449.99, 30, "Professional-grade blender"),
        ("Le Creuset Dutch Oven", 349.99, 15, "Cast iron cooking pot"),
        ("Roomba j7+", 799.99, 12, "Self-emptying robot vacuum")
    ]
    home_kitchen_images = [
        "https://images.unsplash.com/photo-1585515320310-259814833f62?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1585515320310-259814833f62?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1556909212-d5b604d0c90d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?w=400&h=400&fit=crop"
    ]
    product_id = 11
    for i, (name, price, inventory, desc) in enumerate(home_kitchen):
        products.append(Product(product_id, name, "Home & Kitchen", price, inventory, desc, home_kitchen_images[i]))
        product_id += 1
    
    # Fashion (10 products)
    fashion = [
        ("Levi's 501 Jeans", 69.99, 120, "Classic straight-leg jeans"),
        ("Nike Air Max 270", 149.99, 80, "Comfortable running shoes"),
        ("Zara Midi Dress", 79.99, 50, "Elegant summer dress"),
        ("Ray-Ban Aviators", 169.99, 60, "Classic sunglasses"),
        ("North Face Jacket", 199.99, 40, "Waterproof outdoor jacket"),
        ("Adidas Ultraboost", 179.99, 70, "Premium running shoes"),
        ("H&M Blazer", 89.99, 55, "Professional blazer"),
        ("Timberland Boots", 189.99, 45, "Durable work boots"),
        ("Calvin Klein Watch", 249.99, 30, "Minimalist wristwatch"),
        ("Patagonia Fleece", 149.99, 50, "Warm outdoor fleece")
    ]
    fashion_images = [
        "https://images.unsplash.com/photo-1542272454315-7f6f20e0e193?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1505691723518-36a5ac3be353?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(fashion):
        products.append(Product(product_id, name, "Fashion", price, inventory, desc, fashion_images[i]))
        product_id += 1
    
    # Books (8 products)
    books = [
        ("Atomic Habits", 16.99, 200, "James Clear's guide to building good habits"),
        ("Sapiens", 18.99, 150, "Yuval Noah Harari's history of humankind"),
        ("Python Crash Course", 39.99, 100, "Hands-on programming guide"),
        ("Thinking, Fast and Slow", 17.99, 120, "Daniel Kahneman on decision making"),
        ("The Lean Startup", 19.99, 90, "Eric Ries on entrepreneurship"),
        ("Clean Code", 44.99, 80, "Robert Martin on software craftsmanship"),
        ("Introduction to Algorithms", 89.99, 50, "CLRS algorithms textbook"),
        ("Designing Data-Intensive Applications", 54.99, 70, "Martin Kleppmann on system design")
    ]
    books_images = [
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1589998059171-988d887df646?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1510172951991-856a654063f9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(books):
        products.append(Product(product_id, name, "Books", price, inventory, desc, books_images[i]))
        product_id += 1
    
    # Sports & Fitness (9 products)
    sports = [
        ("Bowflex Dumbbells", 349.99, 25, "Adjustable weight dumbbells"),
        ("Peloton Bike", 1445.00, 10, "Interactive fitness bike"),
        ("Yoga Mat Premium", 49.99, 100, "Non-slip exercise mat"),
        ("Fitbit Charge 6", 159.99, 60, "Advanced fitness tracker"),
        ("Resistance Bands Set", 29.99, 150, "Versatile workout bands"),
        ("Protein Powder (5lb)", 59.99, 80, "Whey protein supplement"),
        ("TRX Suspension Trainer", 179.99, 40, "Bodyweight training system"),
        ("Foam Roller", 34.99, 90, "Muscle recovery tool"),
        ("Jump Rope", 19.99, 120, "Speed jump rope for cardio")
    ]
    sports_images = [
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1579722820308-d74e571900a9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1520877880798-5ee004e3f11e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1552196563-55cd4e45efb3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(sports):
        products.append(Product(product_id, name, "Sports & Fitness", price, inventory, desc, sports_images[i]))
        product_id += 1
    
    # Beauty & Personal Care (9 products)
    beauty = [
        ("CeraVe Moisturizer", 19.99, 200, "Hydrating facial moisturizer"),
        ("The Ordinary Serum", 24.99, 150, "Niacinamide + Zinc serum"),
        ("Dyson Airwrap", 599.99, 15, "Multi-styler hair tool"),
        ("Olaplex Hair Treatment", 28.00, 100, "Bond-building hair care"),
        ("Neutrogena Sunscreen SPF 50", 12.99, 180, "Broad spectrum sun protection"),
        ("Gillette Fusion Razor", 29.99, 120, "5-blade shaving system"),
        ("Oral-B Electric Toothbrush", 89.99, 70, "Rechargeable toothbrush"),
        ("Cetaphil Cleanser", 14.99, 160, "Gentle facial cleanser"),
        ("Revlon Hair Dryer", 59.99, 50, "One-step hair dryer and volumizer")
    ]
    beauty_images = [
        "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1532413992378-f169ac26fff0?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1499857177096-9ab90f728f04?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(beauty):
        products.append(Product(product_id, name, "Beauty & Personal Care", price, inventory, desc, beauty_images[i]))
        product_id += 1
    
    # Toys & Games (8 products)
    toys = [
        ("LEGO Star Wars Set", 129.99, 40, "Millennium Falcon building set"),
        ("Monopoly Board Game", 24.99, 80, "Classic family board game"),
        ("Nintendo Switch", 299.99, 35, "Hybrid gaming console"),
        ("PlayStation 5", 499.99, 8, "Next-gen gaming console"),
        ("Rubik's Cube", 14.99, 150, "Classic 3x3 puzzle cube"),
        ("Nerf Elite Blaster", 39.99, 70, "Foam dart blaster"),
        ("Hot Wheels Track Set", 49.99, 60, "Racing track playset"),
        ("Barbie Dreamhouse", 199.99, 20, "Dollhouse playset")
    ]
    toys_images = [
        "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587654780333-21f06ca2f408?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1525857597365-5f6dbff2e36e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1563396983906-b3795482a59a?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(toys):
        products.append(Product(product_id, name, "Toys & Games", price, inventory, desc, toys_images[i]))
        product_id += 1
    
    # Automotive (8 products)
    automotive = [
        ("Dash Cam 4K", 129.99, 50, "Front and rear dash camera"),
        ("Car Phone Mount", 24.99, 100, "Magnetic phone holder"),
        ("WeatherTech Floor Mats", 149.99, 40, "All-weather car mats"),
        ("Michelin Wiper Blades", 29.99, 80, "Premium windshield wipers"),
        ("Portable Jump Starter", 79.99, 60, "Emergency battery pack"),
        ("Turtle Wax Car Wash Kit", 34.99, 90, "Complete car cleaning set"),
        ("Craftsman Tool Set", 199.99, 30, "Mechanics tool set"),
        ("Car Vacuum Cleaner", 49.99, 70, "Portable handheld vacuum")
    ]
    automotive_images = [
        "https://images.unsplash.com/photo-1590362891991-f776e747a588?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519558260268-cde7e03a0152?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1610647752706-3bb12232b3ab?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1604921191928-661a527f5b48?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1607860108855-64acf2078ed9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1581235720704-06d3acfcb36f?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(automotive):
        products.append(Product(product_id, name, "Automotive", price, inventory, desc, automotive_images[i]))
        product_id += 1
    
    # Office Supplies (9 products)
    office = [
        ("Herman Miller Aeron Chair", 1395.00, 12, "Ergonomic office chair"),
        ("Standing Desk Electric", 599.99, 18, "Height-adjustable desk"),
        ("LG 27\" 4K Monitor", 399.99, 35, "Ultra HD display"),
        ("Logitech MX Master 3", 99.99, 80, "Wireless ergonomic mouse"),
        ("Mechanical Keyboard RGB", 149.99, 60, "Gaming/productivity keyboard"),
        ("Moleskine Notebook", 19.99, 150, "Classic hardcover notebook"),
        ("Sharpie Markers (24-pack)", 14.99, 200, "Permanent markers"),
        ("Stapler Heavy Duty", 29.99, 100, "Professional stapler"),
        ("Paper Shredder", 89.99, 40, "Cross-cut document shredder")
    ]
    office_images = [
        "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1595492379543-77dd7ba47f82?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1565024354253-685b44f06f4b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587293852726-70cdb56c2866?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(office):
        products.append(Product(product_id, name, "Office Supplies", price, inventory, desc, office_images[i]))
        product_id += 1
    
    # Health & Wellness (10 products)
    health = [
        ("Vitamin D3 5000 IU", 19.99, 150, "Daily vitamin supplement"),
        ("Omega-3 Fish Oil", 24.99, 120, "Heart health supplement"),
        ("Multivitamin Gummies", 16.99, 180, "Daily nutrition gummies"),
        ("Meditation Cushion", 49.99, 60, "Zafu meditation pillow"),
        ("Essential Oil Diffuser", 39.99, 90, "Aromatherapy diffuser"),
        ("Heating Pad Electric", 34.99, 70, "Pain relief heating pad"),
        ("Blood Pressure Monitor", 59.99, 50, "Digital BP monitor"),
        ("Massage Gun", 149.99, 40, "Percussion therapy device"),
        ("Sleep Mask Silk", 24.99, 100, "Comfortable eye mask"),
        ("White Noise Machine", 49.99, 65, "Sleep sound machine")
    ]
    health_images = [
        "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1512438248247-f0f2a5a8b7f0?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1631730486572-226d1f595b68?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1615486511262-60a4b7114906?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1573461160327-b450ce3d8e7f?w=400&h=400&fit=crop"
    ]
    for i, (name, price, inventory, desc) in enumerate(health):
        products.append(Product(product_id, name, "Health & Wellness", price, inventory, desc, health_images[i]))
        product_id += 1
    
    return products


def get_sample_users() -> List[User]:
    """
    Get all 20 users with purchase histories and preferences.
    
    Returns:
        List of User objects
    """
    user_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve",
        "Frank", "Grace", "Henry", "Iris", "Jack",
        "Kate", "Leo", "Mia", "Noah", "Olivia",
        "Paul", "Quinn", "Rachel", "Sam", "Tina"
    ]
    
    users = []
    for i, name in enumerate(user_names, 1):
        user_id = f"U{i:03d}"
        users.append(User(
            id=user_id,
            name=name,
            purchase_history=[],  # Will be populated from transactions
            viewed_products=[],
            preferred_categories=set(),
            cart_items=[]  # Always starts empty
        ))
    
    return users


def get_sample_transactions() -> List[Transaction]:
    """
    Get 100 realistic transactions with co-purchase patterns.
    
    Returns:
        List of Transaction objects
    """
    transactions = []
    
    # Define affinity groups (products often bought together)
    affinity_groups = [
        # Apple ecosystem
        [1, 3, 4, 5],  # iPhone, iPad, Apple Watch, AirPods
        [1, 5, 7],  # iPhone, AirPods, Sony Headphones
        [2, 3, 5],  # MacBook, iPad, AirPods
        [2, 43, 44, 45],  # MacBook + Monitor, Mouse, Keyboard
        [4, 5],  # Apple Watch, AirPods
        
        # Samsung ecosystem
        [6, 7],  # Samsung phone, Sony headphones
        
        # Photography/Content creation
        [10, 2],  # Canon Camera + MacBook
        [10, 8],  # Canon Camera + Dell laptop
        
        # Tech enthusiast
        [8, 9, 7],  # Dell laptop, LG TV, Sony headphones
        [9, 62, 63],  # LG TV + Gaming consoles
        
        # Home cooking
        [11, 12, 13, 16],  # Instant Pot, Air Fryer, KitchenAid, Vitamix
        
        # Fitness bundle
        [46, 48, 49, 50],  # Dumbbells, Yoga Mat, Fitbit, Resistance Bands
        [47, 48, 51],  # Peloton, Yoga Mat, Protein Powder
        
        # Gaming setup
        [43, 44, 45, 62, 63],  # Monitor, Mouse, Keyboard, Nintendo Switch, PS5
        [9, 62],  # TV + Nintendo Switch
        [9, 63],  # TV + PS5
        
        # Running gear
        [22, 23, 48],  # Nike shoes, Adidas shoes, Fitbit
        
        # Home office
        [37, 38, 43, 44, 45],  # Herman Miller chair, Standing desk, Monitor, Mouse, Keyboard
        [2, 37, 38],  # MacBook + chair + standing desk
        [8, 44, 45],  # Dell laptop + Mouse + Keyboard
        
        # Beauty routine
        [55, 56, 59, 60],  # CeraVe, The Ordinary, Sunscreen, Cleanser
        
        # Book bundle (learning)
        [31, 33, 35, 36],  # Atomic Habits, Python Crash Course, Clean Code, Algorithms
        [32, 33],  # Sapiens + Python Crash Course
        
        # Car care
        [69, 72, 74, 76],  # Dash cam, Wiper blades, Jump starter, Car wash kit
    ]
    
    # Generate 100 transactions
    user_ids = [f"U{i:03d}" for i in range(1, 21)]
    
    # 70 transactions from affinity groups (more realistic patterns)
    for _ in range(70):
        user_id = random.choice(user_ids)
        group = random.choice(affinity_groups)
        # Buy 2-4 items from the group
        num_items = random.randint(2, min(4, len(group)))
        product_ids = random.sample(group, num_items)
        transactions.append(Transaction(user_id, product_ids))
    
    # 30 random transactions (1-2 items) for diversity
    for _ in range(30):
        user_id = random.choice(user_ids)
        num_items = random.randint(1, 2)
        product_ids = random.sample(range(1, 90), num_items)
        transactions.append(Transaction(user_id, product_ids))
    
    return transactions


def initialize_user_data(users: List[User], transactions: List[Transaction], products: List[Product]) -> None:
    """
    Initialize user purchase histories and preferred categories from transactions.
    
    Args:
        users: List of users
        transactions: List of transactions
        products: List of products
    """
    # Create user lookup
    user_map = {user.id: user for user in users}
    product_map = {product.id: product for product in products}
    
    # Process transactions
    for transaction in transactions:
        user = user_map.get(transaction.user_id)
        if user:
            for product_id in transaction.product_ids:
                # Add to purchase history
                if product_id not in user.purchase_history:
                    user.purchase_history.append(product_id)
                
                # Add category to preferences
                product = product_map.get(product_id)
                if product:
                    user.preferred_categories.add(product.category)
                    
                    # Increment product purchase count
                    product.purchases += 1
    
    # Add some viewed products (products they viewed but didn't buy)
    for user in users:
        # Each user views 5-10 additional products
        num_views = random.randint(5, 10)
        all_product_ids = list(range(1, 90))
        # Remove already purchased products
        available_products = [pid for pid in all_product_ids if pid not in user.purchase_history]
        viewed = random.sample(available_products, min(num_views, len(available_products)))
        user.viewed_products = viewed
        
        # Increment view count
        for product_id in viewed:
            product = product_map.get(product_id)
            if product:
                product.views += 1


def get_all_categories() -> List[str]:
    """Get list of all product categories"""
    return [
        "Electronics",
        "Home & Kitchen",
        "Fashion",
        "Books",
        "Sports & Fitness",
        "Beauty & Personal Care",
        "Toys & Games",
        "Automotive",
        "Office Supplies",
        "Health & Wellness"
    ]
