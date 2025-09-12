from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the store with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating store with sample data...')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest electronic gadgets and devices'},
            {'name': 'Clothing', 'description': 'Fashion and apparel for all ages'},
            {'name': 'Books', 'description': 'Books across various genres'},
            {'name': 'Home & Garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {
                'name': 'Wireless Bluetooth Headphones',
                'category': 'Electronics',
                'description': 'High-quality wireless headphones with noise cancellation and long battery life.',
                'price': 99.99,
                'stock': 50
            },
            {
                'name': 'Smartphone Stand',
                'category': 'Electronics',
                'description': 'Adjustable smartphone stand for desk use, compatible with all phone sizes.',
                'price': 19.99,
                'stock': 100
            },
            {
                'name': '4K Webcam',
                'category': 'Electronics',
                'description': 'Ultra HD webcam perfect for video calls and streaming.',
                'price': 129.99,
                'stock': 25
            },
            
            # Clothing
            {
                'name': 'Cotton T-Shirt',
                'category': 'Clothing',
                'description': '100% organic cotton t-shirt, available in multiple colors.',
                'price': 24.99,
                'stock': 200
            },
            {
                'name': 'Denim Jeans',
                'category': 'Clothing',
                'description': 'Classic fit denim jeans, durable and comfortable.',
                'price': 59.99,
                'stock': 75
            },
            {
                'name': 'Hoodie Sweatshirt',
                'category': 'Clothing',
                'description': 'Warm and cozy hoodie perfect for casual wear.',
                'price': 45.99,
                'stock': 80
            },
            
            # Books
            {
                'name': 'Programming Python',
                'category': 'Books',
                'description': 'Comprehensive guide to Python programming for beginners and experts.',
                'price': 39.99,
                'stock': 30
            },
            {
                'name': 'The Art of Design',
                'category': 'Books',
                'description': 'Explore the principles of good design in this beautifully illustrated book.',
                'price': 29.99,
                'stock': 40
            },
            
            # Home & Garden
            {
                'name': 'Plant Pot Set',
                'category': 'Home & Garden',
                'description': 'Set of 3 ceramic plant pots in different sizes with drainage holes.',
                'price': 34.99,
                'stock': 60
            },
            {
                'name': 'LED Desk Lamp',
                'category': 'Home & Garden',
                'description': 'Adjustable LED desk lamp with touch control and USB charging port.',
                'price': 49.99,
                'stock': 45
            },
            
            # Sports & Outdoors
            {
                'name': 'Yoga Mat',
                'category': 'Sports & Outdoors',
                'description': 'Non-slip yoga mat perfect for home workouts and studio sessions.',
                'price': 29.99,
                'stock': 90
            },
            {
                'name': 'Water Bottle',
                'category': 'Sports & Outdoors',
                'description': 'Insulated stainless steel water bottle, keeps drinks cold for 24 hours.',
                'price': 22.99,
                'stock': 120
            },
        ]

        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'slug': slugify(prod_data['name']),
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'available': True
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated store with sample data!')
        )