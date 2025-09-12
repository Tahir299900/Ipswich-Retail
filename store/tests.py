from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Category, Product, Order, OrderItem
from .cart import Cart

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
            description="Electronic gadgets"
        )
    
    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.slug, "electronics")
        self.assertEqual(str(self.category), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            description="High-performance laptop",
            price=Decimal('999.99'),
            stock=10
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, Decimal('999.99'))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.available)
        self.assertEqual(str(self.product), "Laptop")

class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            description="High-performance laptop",
            price=Decimal('999.99'),
            stock=10
        )
    
    def test_cart_add_product(self):
        from django.http import HttpRequest
        request = HttpRequest()
        request.session = self.client.session
        cart = Cart(request)
        cart.add(self.product, quantity=2)
        
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('1999.98'))

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            description="High-performance laptop",
            price=Decimal('999.99'),
            stock=10
        )
    
    def test_product_list_view(self):
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
    
    def test_product_detail_view(self):
        response = self.client.get(
            reverse('store:product_detail', kwargs={'slug': 'laptop'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
        self.assertContains(response, "999.99")
    
    def test_cart_add_view(self):
        response = self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 1}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after adding
    
    def test_checkout_view_requires_login(self):
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_checkout_view_with_login(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Add product to cart first
        self.client.post(
            reverse('store:cart_add', kwargs={'product_id': self.product.id}),
            {'quantity': 1}
        )
        
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            category=self.category,
            description="High-performance laptop",
            price=Decimal('999.99'),
            stock=10
        )
        self.order = Order.objects.create(
            user=self.user,
            order_id="TEST123",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            address="123 Test St",
            postal_code="12345",
            city="Test City",
            total_cost=Decimal('999.99')
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('999.99'),
            quantity=1
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.order_id, "TEST123")
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_cost, Decimal('999.99'))
    
    def test_order_item_cost(self):
        self.assertEqual(self.order_item.get_cost(), Decimal('999.99'))
    
    def test_order_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), Decimal('999.99'))
